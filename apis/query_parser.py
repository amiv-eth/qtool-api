from flask import request

from flask_restplus import abort

from sqlalchemy import desc, or_, and_
from sqlalchemy.orm import relationship, joinedload

from ast import literal_eval

from marshmallow import Schema, fields

class QuerySchema(Schema):
    where = fields.Str()
    sort = fields.Str()
    page = fields.Int()
    embedded = fields.Str()
    

def queryParser(dbClass = None, embeddingSchema = None):
    arguments = request.args.to_dict()
    schema = QuerySchema()
    query = schema.load(arguments)[0]
    args = {}
    embedding = None
    if 'page' in query:
        args['page'] = query['page']

    if 'embedded' in query:
        try:
            embeddingDict = literal_eval(query['embedded'])
        except:
            abort(400, 'Invalid syntax for query parameter embedded, please pass a valid dicitionary.')
        if not (type(embeddingDict) is dict):
            abort(400, 'Invalid syntax for query parameter embedded, please pass a valid dicitionary.')
        embedding = embeddingParser(embeddingDict, dbClass)
        args['embedded'] = embedding 

    if 'where' in query:
        try:
            whereDict = literal_eval(query['where'])
        except:
            abort(400, 'Invalid syntax for query parameter where, please pass a valid dicitionary.')
        if not (type(whereDict) is dict):
            abort(400, 'Invalid syntax for query parameter where, please pass a valid dicitionary.')
        args['where'] = filterParser(whereDict,dbClass, embedding)

    if 'sort' in query:
        args['sort'] = sortingParser(query['sort'],dbClass, embedding)

    return args


def filterParser(whereStatement,dbClass, embedding):
    if len(whereStatement) > 1:
        abort(400, 'Invalid syntax for query parameter where, wrong number of arguments!')
    
    key = [k for k in whereStatement][0]
    if 'and' == key:
        filterList = whereStatement[key]
        if not (type(filterList) is list):
            abort(400, 'Invalid syntax for query parameter where. An and statement requires a list of dicitionaries!')
        filterCondition = True
        for statement in filterList:
            filterCondition = and_(filterCondition, filterParser(statement, dbClass, embedding))

    elif 'or' == key:
        filterList = whereStatement[key]
        if not (type(filterList) is list):
            abort(400, 'Invalid syntax for query parameter where. An or statement requires a list of dicitionaries!')
        filterCondition = False
        for statement in filterList:
            filterCondition = or_(filterCondition, filterParser(statement, dbClass, embedding))
        # Ensure consistent results, when receiving an empty or statement.
        if len(filterList) == 0:
            filterCondition = True

    else:
        filterCondition = createFilterCondition(key,whereStatement[key], dbClass, embedding)
            
    return filterCondition

def createFilterCondition(condition, val, dbClass, embedding):
    parameters = condition.split('.')
    embeddedKey = None
    if len(parameters) == 1:
        abort(400, 'Invalid syntax for query parameter where, operator missing!')
    elif len(parameters) == 2:
        [attr, op] = parameters
    elif len(parameters) == 3:
        [embeddedKey, attr, op] = parameters
    else:
        abort(400, 'Invalid syntax for query parameter where, to many arguments given!')
    if embeddedKey:
        if embeddedKey in embedding:
            dbClass = embedding[embeddedKey]().databaseName
        else:
            abort(400, 'Invalid syntax for query parameter where, invalid key for embedded data given! The key might be correct, but the data not embedded.')
    # ToDo: schema load for input validation
    if op == "eq":
        condition = getattr(dbClass, attr) == val
    elif op == 'neq':
        condition = getattr(dbClass, attr) != val
    elif op == 'lte':
        condition = getattr(dbClass, attr) <= val
    elif op == 'gte':
        condition = getattr(dbClass, attr) >= val
    elif op == 'in':
        condition = getattr(dbClass, attr)
        condition = condition.contains(val)
    else:
        abort(400, 'Invalid syntax for query parameter where, ' + op + ' is not a valid operator!')

    return condition



def sortingParser(sortingKey,dbClass, embedding):
    errorMessage = 'Invalid sorting parameter. The following syntax is expected: parameter.asc or parameter.desc. If you want to filter by an embedded value use: embedded.parameter.ordering.'
    parameters = sortingKey.split('.')
    embeddedKey = None
    if len(parameters) == 2:
        [key, ordering] = parameters
    elif len(parameters) == 3:
        [embeddedKey, key, ordering] = parameters
    else:
        abort(400, errorMessage)
    try:
        if embeddedKey:
            dbClass = embedding[embeddedKey]().databaseName
        sortingParameter = getattr(dbClass, key)
        if ordering == 'asc':
            return sortingParameter
        elif ordering == 'desc':
            return desc(sortingParameter)
        else:
            abort(400, errorMessage)
    except:
        abort(400, errorMessage)

def embeddingParser(embeddingDict,dbClass):
    joinedLoadList = []
    for key in embeddingDict:
        if embeddingDict[key]:
            if not hasattr(dbClass, key):
                abort(400, 'Invalid syntax for query parameter embedding, ' + key + ' is not a valid attribute!')
            if type((getattr(dbClass,key).property)) != type(relationship(None)):
                abort(400, 'Invalid syntax for query parameter embedding, ' + key + ' is not a related resource!')
            joinedLoadList.append(joinedload(key))
    return tuple(joinedLoadList)