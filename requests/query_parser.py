from flask import request

from schemas.query import QuerySchema

def queryParser():
    arguments = request.args.to_dict()
    querySchema = QuerySchema()
    return (querySchema.load(arguments)[0])