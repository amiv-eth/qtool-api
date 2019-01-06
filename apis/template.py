from .utility import schemaToDict

from requests.query_parser import queryParser

from requests.request import DatabaseRequest



class EndpointConfiguration():
    dbRequest = DatabaseRequest()
    def __init__(self, api, path, access, schema, embeddable):
        self.api = api
        self.path = path
        self.database = access.databaseName
        self.access = access
        self.schema = schema()
        self.embeddable = embeddable
        self.model = api.model(path.title(), schemaToDict(schema))


    def getRequest(self, user):
        args = queryParser(self.database, self.embeddable)
        res = self.dbRequest.getSerializedResponse(user, self.access, **args)
        return res, 200

    def postRequest(self,user):
        self.schema.load_commit(self.api.payload)
        return {'result': self.path.title() + ' added.'}, 201

    def getRequestById(self,user,id):
        accessData = self.access(user)
        return self.dbRequest.getSerializedElementById(id,accessData)

    def patchRequestById(self,user,id):
        accessData = self.access(user)
        newData = self.schema.load(self.api.payload)[0]
        return self.dbRequest.patchElement(id,accessData,newData)

