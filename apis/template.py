from .utility import authenticate, schemaToDict, queryDocumentation

from flask_restplus import Resource, Namespace

from requests.query_parser import queryParser
from requests.request import DatabaseRequest

"""
dbRequest = DatabaseRequest()
api = Namespace('Dummy')

class EndpointTemplate():

    def __init__(self, api, path, database, access, schema, embeddable):
        model = api.model(path.title(), schemaToDict(schema))


class GeneralEndpoint(Resource):
    model = None
    api = api
    def __init__(self, api, path, database, access, schema, embeddable):
        self.api = api
        self.path = path
        self.database = database
        self.access = access
        self.schema = schema
        self.embeddable = embeddable
        self.model = api.model(path.title(), schemaToDict(schema))

    @api.doc(params = queryDocumentation, security='amivapitoken')
    @authenticate()
    def get(self,user):
        args = queryParser(self.database, self.embeddable)
        res = dbRequest.getSerializedResponse(user, self.access, **args)
        return res, 200

    @api.doc(security='amivapitoken')
    @api.expect(model)
    @authenticate(requiredUserLevelBit = [9])
    def post(self, user):
        self.schema.load_commit(self.api.payload)
        return {'result': self.name + ' added.'}, 201

class GeneralEndpointById(Resource):
    model = None
    api = api
    def __init__(self, api, path, database, access, schema, embeddable):
        self.api = api
        self.path = path
        self.database = database
        self.access = access
        self.schema = schema
        self.embeddable = embeddable
        self.model = api.model(path.title(), schemaToDict(schema))

    @api.doc(security='amivapitoken')
    @authenticate()
    def get(self,id,user):
        accessData = self.access(user)
        return dbRequest.getSerializedElementById(id,accessData)

    @api.expect(model)
    @api.doc(security='amivapitoken')
    @authenticate(requiredUserLevelBit = [9])
    def patch(self,id,user):
        accessData = self.access(user)
        newData = self.schema.load(self.api.payload)[0]
        return dbRequest.patchElement(id,accessData,newData)
"""