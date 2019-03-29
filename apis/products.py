from flask_restplus import Namespace, Resource

from .utility import authenticate, queryDocumentation
from .template import EndpointConfiguration

from access.products_access import InvoiceArticleAccess


api = Namespace('Products', path='/products', description='Operations to alter product ressources.')


invoiceArticleConfiguration = EndpointConfiguration(api, 'invoiceArticle', InvoiceArticleAccess(), None)

@api.route('/'+invoiceArticleConfiguration.path)
@api.doc(security = 'amivapitoken')
class InvoiceArticleEndpoint(Resource):
    @api.doc(params=queryDocumentation)
    @authenticate()
    def get(self,user):
        return invoiceArticleConfiguration.getRequest(user)
        
    @api.expect(invoiceArticleConfiguration.model)
    @authenticate(requiredUserLevelBit = [9])
    def post(self, user):
        return invoiceArticleConfiguration.postRequest(user)

@api.route('/'+invoiceArticleConfiguration.path+'/<string:id>')
@api.doc(security = 'amivapitoken')
class InvoiceArticleEndpointById(Resource):
    @authenticate()
    def get(self,id,user):
        return invoiceArticleConfiguration.getRequestById(user,id)

    @api.expect(invoiceArticleConfiguration.model)
    @authenticate(requiredUserLevelBit = [9])
    def patch(self,id,user):
        return invoiceArticleConfiguration.patchRequestById(user,id)