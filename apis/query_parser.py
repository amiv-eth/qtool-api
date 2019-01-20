from flask import request

from flask_restplus import abort

from sqlalchemy import desc, or_, and_

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
    if 'page' in query:
        args['page'] = query['page']

    if 'where' in query:
        try:
            whereDict = literal_eval(query['where'])
        except:
            abort(400, 'Invalid syntax for query parameter where, please pass a valid dicitionary.')
        if not (type(whereDict) is dict):
            abort(400, 'Invalid syntax for query parameter where, please pass a valid dicitionary.')
        args['where'] = filterParser(whereDict,dbClass)

    if 'sort' in query:
        args['sort'] = sortingParser(query['sort'],dbClass)

    if 'embedded' in query:
        try:
            embeddingDict = literal_eval(query['embedded'])
        except:
            abort(400, 'Invalid syntax for query parameter embedded, please pass a valid dicitionary.')
        if not (type(embeddingDict) is dict):
            abort(400, 'Invalid syntax for query parameter embedded, please pass a valid dicitionary.')
        args['embedded'] = embeddingParser(embeddingDict, embeddingSchema)

    return args


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
    [attr, op] = condition.split('.')
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



def sortingParser(sortingKey,dbClass):
    try:
        [key,ordering] = sortingKey.split('.')
        sortingParameter = getattr(dbClass, key)
        if ordering == 'asc':
            return sortingParameter
        elif ordering == 'desc':
            return desc(sortingParameter)
    except:
        abort(400, 'Invalid sorting parameter. The following syntax is expected: parameter.asc or parameter.desc.')

def embeddingParser(embeddingDict,embeddingSchema):
    if not embeddingSchema:
        return {}
    schema = embeddingSchema()
    embedding = schema.load(embeddingDict)[0]
    return embedding