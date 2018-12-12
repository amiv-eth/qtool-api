from flask_restplus import Namespace, Resource

from .utility import authenticate, schemaToDict


from requests.request import DatabaseRequest
from requests.utility_access import AccountAccess, CategoryAccess, CurrencyAccess, TypeAccess

from schemas.transaction_utility import TransactionTypeSchema, TransactionCurrencySchema, TransactionCategorySchema, TransactionAccountSchema


api = Namespace('Transaction Utility', path='/utility', description='Operations to alter transaction utility ressources.')

dbRequest = DatabaseRequest()



def generalizedRessource(path, schemaClass, access):
    schema = schemaClass()
    model = api.model(path.title(), schemaToDict(schema))
    @api.route('/'+path)
    class className(Resource):
        @api.doc(security='amivapitoken')
        @authenticate()
        def get(self,user):
            accessData = access(user)
            res = dbRequest.getSerializedElements(accessData)
            return res, 200

        @api.doc(security='amivapitoken')
        @api.expect(model)
        @authenticate(requiredUserLevelBit = [9])
        def post(self, user):
            schema.load_commit(api.payload)
            return {'result': path.title() + ' added.'}, 201

    @api.route('/'+path+'/<string:id>')
    class classNameId(Resource):
        @api.doc(security='amivapitoken')
        @authenticate()
        def get(self,id,user):
            accessData = access(user)
            return dbRequest.getSerializedElementById(id,accessData)

        @api.expect(model)
        @api.doc(security='amivapitoken')
        @authenticate(requiredUserLevelBit = [9])
        def patch(self,id,user):
            accessData = access(user)
            newData = schema.load(api.payload)[0]
            return dbRequest.patchElement(id,accessData,newData)


accountRessource = generalizedRessource('account', TransactionAccountSchema,AccountAccess)
categoryRessource = generalizedRessource('category', TransactionCategorySchema, CategoryAccess)
currencyRessource = generalizedRessource('currency', TransactionCurrencySchema, CurrencyAccess)
typeRessource = generalizedRessource('type', TransactionTypeSchema, TypeAccess)


"""

class generalEndpoint(Resource):
    model = "Default"

    @api.doc(security='amivapitoken')
    @authenticate()
    def get(self,user):
        accessData = self.access(user)
        res = dbRequest.getSerializedElements(accessData)
        return res, 200

    @api.doc(security='amivapitoken')
    @api.expect(model)
    @authenticate(requiredUserLevelBit = [9])
    def post(self, user):
        self.schema.load_commit(api.payload)
        return {'result': self.name + ' added.'}, 201

class generalEndpointById(Resource):
    model = "Default"

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
        newData = self.schema.load(api.payload)[0]
        return dbRequest.patchElement(id,accessData,newData)

@api.route('/account')
class Account(generalEndpoint):
    access = AccountAccess
    name = "Account"
    schema = TransactionAccountSchema()
    model = api.model(name, schemaToDict(schema))

@api.route('/account/<string:id>')
class AccountById(generalEndpointById):
    access = AccountAccess
    name = "Account"
    schema = TransactionAccountSchema()
    model = api.model(name, schemaToDict(schema))

"""
