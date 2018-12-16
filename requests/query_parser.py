from flask import request

from flask_restplus import abort

from sqlalchemy import desc

from schemas.query import QuerySchema

def queryParser(dbClass = None):
    arguments = request.args.to_dict()
    querySchema = QuerySchema()
    query = querySchema.load(arguments)[0]
    print(query)
    args = {}
    if 'page' in query:
        args['page'] = query['page']
    if 'where' in query:
        filterParser(query['where'],dbClass)
    if 'sort' in query:
        args['sort'] = sortingParser(query['sort'],dbClass)
    return args

def filterParser(whereStatement,dbClass):
    print(query)
    pass

def sortingParser(sortingKey,dbClass):
    try:
        [key,ordering] = sortingKey.split('.')
        print (key,ordering)
        sortingParameter = getattr(dbClass, key)
        if ordering == 'asc':
            return sortingParameter
        elif ordering == 'desc':
            return desc(sortingParameter)
    except:
        abort(400, 'Invalid sorting parameter. The following syntax is expected: parameter.asc or parameter.desc.')

def embeddingParser(query,dbClass):
    pass