from flask_restplus import Namespace, Resource

from .utility import authenticate, queryDocumentation
from .template import EndpointConfiguration

from access.utility_access import AccountAccess, CategoryAccess, CurrencyAccess, TypeAccess


api = Namespace('Transaction Utility', path='/utility', description='Operations to alter transaction utility ressources.')


accountConfiguration = EndpointConfiguration(api, 'account', AccountAccess(), None)

@api.route('/'+accountConfiguration.path)
@api.doc(security = 'amivapitoken')
class AccountEndpoint(Resource):
    @api.doc(params=queryDocumentation)
    @authenticate()
    def get(self,user):
        return accountConfiguration.getRequest(user)
        
    @api.expect(accountConfiguration.model)
    @authenticate(requiredUserLevelBit = [9])
    def post(self, user):
        return accountConfiguration.postRequest(user)

@api.route('/'+accountConfiguration.path+'/<string:id>')
@api.doc(security = 'amivapitoken')
class AccountEndpointById(Resource):
    @authenticate()
    def get(self,id,user):
        return accountConfiguration.getRequestById(user,id)

    @api.expect(accountConfiguration.model)
    @authenticate(requiredUserLevelBit = [9])
    def patch(self,id,user):
        return accountConfiguration.patchRequestById(user,id)


categoryConfiguration = EndpointConfiguration(api, 'category', CategoryAccess(), None)

@api.route('/'+categoryConfiguration.path)
@api.doc(security = 'amivapitoken')
class CategoryEndpoint(Resource):
    @api.doc(params=queryDocumentation)
    @authenticate()
    def get(self,user):
        return categoryConfiguration.getRequest(user)
        
    @api.expect(categoryConfiguration.model)
    @authenticate(requiredUserLevelBit = [9])
    def post(self, user):
        return categoryConfiguration.postRequest(user)

@api.route('/'+categoryConfiguration.path+'/<string:id>')
@api.doc(security = 'amivapitoken')
class CategoryEndpointById(Resource):
    @authenticate()
    def get(self,id,user):
        return categoryConfiguration.getRequestById(user,id)

    @api.expect(categoryConfiguration.model)
    @authenticate(requiredUserLevelBit = [9])
    def patch(self,id,user):
        return categoryConfiguration.patchRequestById(user,id)


currencyConfiguration = EndpointConfiguration(api, 'currency', CurrencyAccess(), None)

@api.route('/'+currencyConfiguration.path)
@api.doc(security = 'amivapitoken')
class CurrencyEndpoint(Resource):
    @api.doc(params=queryDocumentation)
    @authenticate()
    def get(self,user):
        return currencyConfiguration.getRequest(user)
        
    @api.expect(currencyConfiguration.model)
    @authenticate(requiredUserLevelBit = [9])
    def post(self, user):
        return currencyConfiguration.postRequest(user)

@api.route('/'+currencyConfiguration.path+'/<string:id>')
@api.doc(security = 'amivapitoken')
class CurrencyEndpointById(Resource):
    @authenticate()
    def get(self,id,user):
        return currencyConfiguration.getRequestById(user,id)

    @api.expect(currencyConfiguration.model)
    @authenticate(requiredUserLevelBit = [9])
    def patch(self,id,user):
        return currencyConfiguration.patchRequestById(user,id)


typeConfiguration = EndpointConfiguration(api, 'type', TypeAccess(), None)

@api.route('/'+typeConfiguration.path)
@api.doc(security = 'amivapitoken')
class TypeEndpoint(Resource):
    @api.doc(params=queryDocumentation)
    @authenticate()
    def get(self,user):
        return typeConfiguration.getRequest(user)
        
    @api.expect(typeConfiguration.model)
    @authenticate(requiredUserLevelBit = [9])
    def post(self, user):
        return typeConfiguration.postRequest(user)

@api.route('/'+typeConfiguration.path+'/<string:id>')
@api.doc(security = 'amivapitoken')
class TypeEndpointById(Resource):
    @authenticate()
    def get(self,id,user):
        return typeConfiguration.getRequestById(user,id)

    @api.expect(typeConfiguration.model)
    @authenticate(requiredUserLevelBit = [9])
    def patch(self,id,user):
        return typeConfiguration.patchRequestById(user,id)
