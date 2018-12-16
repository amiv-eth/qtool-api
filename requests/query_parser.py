from flask import request

from marshmallow import fields

from flask_restplus import abort

from sqlalchemy import desc

from ast import literal_eval

from schemas.query import QuerySchema
from schemas.transaction import TransactionSchema

def queryParser(dbClass = None, embeddingSchema = None):
    arguments = request.args.to_dict()
    schema = QuerySchema()
    query = schema.load(arguments)[0]
    print(query)
    args = {}
    if 'page' in query:
        args['page'] = query['page']
    if 'where' in query:
        filterParser(query['where'],dbClass)
    if 'sort' in query:
        args['sort'] = sortingParser(query['sort'],dbClass)
    if 'embedded' in query:
        embeddingDict = literal_eval(query['embedded'])
        embeddingParser(embeddingDict, embeddingSchema)
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

def embeddingParser(embeddingDict,embeddingSchema):
    schema = embeddingSchema()
    print(embeddingDict)
    embedding = schema.load(embeddingDict)[0]
    print (embedding)