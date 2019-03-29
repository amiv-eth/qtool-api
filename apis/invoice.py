from flask_restplus import Namespace, Resource

from .utility import authenticate, queryDocumentation

from .template import EndpointConfiguration


from access.invoice_access import InvoiceAccess, InvoiceEmbeddable, InvoiceItemAccess, InvoiceItemEmbeddable

api = Namespace('Invoice', description='Invoice related operations.')

invoiceConfiguration = EndpointConfiguration(api, 'invoice', InvoiceAccess(), InvoiceEmbeddable())

@api.route('/'+invoiceConfiguration.path)
@api.doc(security = 'amivapitoken')
class InvoiceEndpoint(Resource):
    @api.doc(params=queryDocumentation)
    @authenticate()
    def get(self,user):
        return invoiceConfiguration.getRequest(user)


invoiceItemConfiguration = EndpointConfiguration(api, 'invoiceItem', InvoiceItemAccess(), InvoiceItemEmbeddable())

@api.route('/'+invoiceItemConfiguration.path)
@api.doc(security = 'amivapitoken')
class AccountEndpoint(Resource):
    @api.doc(params=queryDocumentation)
    @authenticate()
    def get(self,user):
        return invoiceItemConfiguration.getRequest(user)
