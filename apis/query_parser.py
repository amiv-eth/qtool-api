from flask import request
from flask_restplus import abort

from sqlalchemy import asc, desc, or_, and_
from sqlalchemy.orm import relationship, joinedload

from ast import literal_eval

from marshmallow import Schema, fields

class QuerySchema(Schema):
    where = fields.Str()
    sort = fields.Str()
    page = fields.Int()
    embedded = fields.Str()


def queryParser(dbClass):
    query = request.args.to_dict()
    query = QuerySchema().load(query).data

    if 'sort' in query:
        query['sort'] = sortParser(dbClass, query['sort'])

    if 'embedded' in query:
        query['embedded'] = embeddingParser(dbClass, query['embedded'])

    if 'where' in query:
        try:
            whereDict = literal_eval(query['where'])
            whereDict = dict(whereDict)
        except:
            abort(400, 'Invalid syntax for query parameter where, please pass a valid dicitionary.')
        query['where'] = filterParser(whereDict,dbClass)

    parameters = {
        "where": True,
        "sort": None,
        "page": 1,
        "embedded": ()
        }
    parameters.update(query)
    return parameters

def decomposeNestedOperator(dbClass, opString):
    parameters = opString.split('.')
    numberOfParameters = len(parameters)
    if numberOfParameters == 3:
        [relation, attribute, operator] = parameters
        try:
            dbClass = getattr(dbClass, relation).property.entity.class_
            relatedDatabase = dbClass
        except:
            errorMessage = '[Query Error]: ' + dbClass.__tablename__ + ' has no related database called '+ relation + '.'
            abort(400, errorMessage)    
    elif numberOfParameters == 2:
        [attribute, operator] = parameters
        relatedDatabase = None
    else: 
        errorMessage = '[Query Error]: Invalid operation: ' + opString + ', the following syntax is expected: (embeddedResource.)attribute.operator.'
        abort(400, errorMessage)
    try:
        attributeInstance = getattr(dbClass, attribute)
    except: 
        errorMessage = '[Query Error]: ' + dbClass.__tablename__ + ' has no attribute called '+ attribute + '.'
        abort(400, errorMessage)
    return (relatedDatabase,attributeInstance,operator)

def sortParser(dbClass, sortingParameter):
    #ToDo: Can not sort by an unloaded related database!
    (relatedDatabase, attribute, operator) = decomposeNestedOperator(dbClass, sortingParameter)
    if operator == 'asc':
        return (asc(attribute),relatedDatabase)
    elif operator == 'desc':
        return (desc(attribute),relatedDatabase)
    else:
        errorMessage = '[Query Error]: ' + operator + ' is no valid sorting order. Use asc or desc.'
        abort(400, errorMessage)

def filterParser(whereStatement,dbClass):
    if len(whereStatement) > 1:
        abort(400, 'Invalid syntax for query parameter where, wrong number of arguments!')
    
    key = [k for k in whereStatement][0]
    if 'and' == key:
        filterList = whereStatement[key]
        if not (type(filterList) is list):
            abort(400, 'Invalid syntax for query parameter where. An and statement requires a list of dicitionaries!')
        filterCondition = True
        for statement in filterList:
            filterCondition = and_(filterCondition, filterParser(statement, dbClass))

    elif 'or' == key:
        filterList = whereStatement[key]
        if not (type(filterList) is list):
            abort(400, 'Invalid syntax for query parameter where. An or statement requires a list of dicitionaries!')
        filterCondition = False
        for statement in filterList:
            filterCondition = or_(filterCondition, filterParser(statement, dbClass))
        # Ensure consistent results, when receiving an empty or statement.
        if len(filterList) == 0:
            filterCondition = True

    else:
        filterCondition = createFilterCondition(key,whereStatement[key], dbClass)
            
    return filterCondition

def createFilterCondition(condition, val, dbClass):
    (secondaryDatabase, attr, op) = decomposeNestedOperator(dbClass, condition)
    # ToDo: schema load for input validation
    if op == "eq":
        condition = attr == val
    elif op == 'neq':
        condition = attr != val
    elif op == 'lte':
        condition = attr <= val
    elif op == 'gte':
        condition = attr >= val
    elif op == 'in':
        condition = attr
        condition = condition.contains(val)
    else:
        abort(400, 'Invalid syntax for query parameter where, ' + op + ' is not a valid operator!')
    return condition

def embeddingParser(dbClass, embedded):
    try:
        embeddingDict = literal_eval(embedded)
        embeddingDict = dict(embeddingDict)
    except:
        abort(400, 'Invalid syntax for query parameter embedded, please pass a valid dicitionary.')
    joinedLoadList = []
    for key in embeddingDict:
        if embeddingDict[key]:
            if not hasattr(dbClass, key):
                abort(400, 'Invalid syntax for query parameter embedding, ' + key + ' is not a valid attribute!')
            if type((getattr(dbClass,key).property)) != type(relationship(None)):
                abort(400, 'Invalid syntax for query parameter embedding, ' + key + ' is not a related resource!')
            joinedLoadList.append(joinedload(key))
    return tuple(joinedLoadList)