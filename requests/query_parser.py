from flask import request

from marshmallow import fields

from flask_restplus import abort

from sqlalchemy import desc

from ast import literal_eval

from schemas.query import QuerySchema
from schemas.transaction import TransactionSchema

def queryParser(dbClass = None, embeddingSchema = None, embeddingQuery = {}):
    arguments = request.args.to_dict()
    schema = QuerySchema()
    query = schema.load(arguments)[0]
    args = {}
    if 'page' in query:
        args['page'] = query['page']
    if 'where' in query:
        filterParser(query['where'],dbClass)
    if 'sort' in query:
        args['sort'] = sortingParser(query['sort'],dbClass)
    if 'embedded' in query:
        try:
            embeddingDict = literal_eval(query['embedded'])
        except:
            abort(400, 'Invalid syntax for query parameter embedded, please pass a valid dicitionary.')
        if not (type(embeddingDict) is dict):
            abort(400, 'Invalid syntax for query parameter embedded, please pass a valid dicitionary.')
        args['embedded'] = embeddingParser(embeddingDict, embeddingSchema, embeddingQuery)
    return args

def filterParser(whereStatement,dbClass):
    transactionSchema = TransactionSchema()
    print(type(whereStatement))
    deserialized = transactionSchema.load(whereStatement)
    print(deserialized)

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

def embeddingParser(embeddingDict,embeddingSchema, embeddingQuery):
    schema = embeddingSchema()
    embedding = schema.load(embeddingDict)[0]
    print (embedding)
    embeddingAccess = {}
    for key in embedding:
        if embedding[key]:
            embeddingAccess[key] = embeddingQuery[key]
    print(embeddingAccess)
    return embeddingAccess