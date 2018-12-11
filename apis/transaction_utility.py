from flask_restplus import Namespace, Resource

from .utility import authenticate, schemaToDict


from requests.request import DatabaseRequest
from requests.utility_access import AccountAccess, CategoryAccess, CurrencyAccess, TypeAccess

from schemas.transaction_utility import TransactionTypeSchema, TransactionCurrencySchema, TransactionCategorySchema, TransactionAccountSchema


api = Namespace('Transaction Utility', path='/utility', description='Operations to alter transaction utility ressources.')

dbRequest = DatabaseRequest()

@api.route('/account')
class Account(Resource):
    @api.doc(security='amivapitoken')
    @authenticate()
    def get(self,user):
        accessData = AccountAccess(user)
        res = dbRequest.getSerializedElements(accessData)
        return res, 200

    @api.doc(security='amivapitoken')
    @api.expect(api.model('Account', schemaToDict(TransactionAccountSchema)))
    @authenticate()
    def post(self, user):
        accountSchema = TransactionAccountSchema()
        accountSchema.load(api.payload)[0]
        return {'result': 'Account added.'}, 201


@api.route('/category')
class Category(Resource):
    @api.doc(security='amivapitoken')
    @authenticate()
    def get(self,user):
        accessData = CategoryAccess(user)
        res = dbRequest.getSerializedElements(accessData)
        return res, 200

    @api.doc(security='amivapitoken')
    @api.expect(api.model('Category', schemaToDict(TransactionCategorySchema)))
    @authenticate()
    def post(self, user):
        categorySchema = TransactionCategorySchema()
        categorySchema.load(api.payload)[0]
        return {'result': 'Category added.'}, 201


@api.route('/currency')
class Currency(Resource):
    @api.doc(security='amivapitoken')
    @authenticate()
    def get(self,user):
        accessData = CurrencyAccess(user)
        res = dbRequest.getSerializedElements(accessData)
        return res, 200

    @api.doc(security='amivapitoken')
    @api.expect(api.model('Currency', schemaToDict(TransactionCurrencySchema)))
    @authenticate()
    def post(self, user):
        currencySchema = TransactionCurrencySchema()
        currencySchema.load(api.payload)[0]
        return {'result': 'Currency added.'}, 201


@api.route('/type')
class Type(Resource):
    @api.doc(security='amivapitoken')
    @authenticate()
    def get(self,user):
        accessData = TypeAccess(user)
        res = dbRequest.getSerializedElements(accessData)
        return res, 200

    @api.doc(security='amivapitoken')
    @api.expect(api.model('Type', schemaToDict(TransactionTypeSchema)))
    @authenticate()
    def post(self, user):
        typeSchema = TransactionTypeSchema()
        typeSchema.load(api.payload)[0]
        return {'result': 'Type added.'}, 201


