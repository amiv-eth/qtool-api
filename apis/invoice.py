from flask_restplus import Namespace, Resource

from .utility import authenticate, queryDocumentation

from sql import db

from .template import EndpointConfiguration

from sqlalchemy.orm import joinedload

from access.invoice_access import InvoiceAccess, InvoiceEmbeddable, InvoiceItemAccess, InvoiceItemEmbeddable

from schemas.invoice import InvoiceSchema, InvoiceItemSchema
from sql.invoice import Invoice, InvoiceItem

api = Namespace('Invoice', description='Invoice related operations.')

invoiceConfiguration = EndpointConfiguration(api, 'invoice', InvoiceAccess(), InvoiceEmbeddable())

@api.route('/'+invoiceConfiguration.path)
@api.doc(security = 'amivapitoken')
class InvoiceEndpoint(Resource):
    @api.doc(params=queryDocumentation)
    @authenticate()
    def get(self,user):
        invoice = Invoice.query.options(joinedload('issuer')).limit(25).all()
        invoice_schema = InvoiceSchema(exclude=('issue_date','issuer.password',),many=True)
        print(invoice_schema._declared_fields)
        return invoice_schema.dump(invoice).data
        """
        return invoiceConfiguration.getRequest(user)
        """

    @api.expect(invoiceConfiguration.model)
    @authenticate(requiredUserLevelBit = [9])
    def post(self, user):
        return invoiceConfiguration.postRequest(user)

@api.route('/'+invoiceConfiguration.path+'/<string:id>')
@api.doc(security = 'amivapitoken')
class InvoiceEndpointById(Resource):
    @authenticate()
    def get(self,id,user):
        return invoiceConfiguration.getRequestById(user,id)

    @api.expect(invoiceConfiguration.model)
    @authenticate(requiredUserLevelBit = [9])
    def patch(self,id,user):
        return invoiceConfiguration.patchRequestById(user,id)

    @authenticate(requiredUserLevelBit = [9])
    def delete(self,id,user):
        invoiceConfiguration.getElementById(id, user).is_valid = False
        db.session.commit()
        return {"message": "Operation successful."}, 202


invoiceItemConfiguration = EndpointConfiguration(api, 'invoiceItem', InvoiceItemAccess(), InvoiceItemEmbeddable())

# ToDo: Post Transaction before invoice item, to obtain a transaction id

@api.route('/'+invoiceItemConfiguration.path)
@api.doc(security = 'amivapitoken')
class InvoiceItemEndpoint(Resource):
    @api.doc(params=queryDocumentation)
    @authenticate()
    def get(self,user):
        return invoiceItemConfiguration.getRequest(user)

    """
    @api.expect(invoiceItemConfiguration.model)
    @authenticate(requiredUserLevelBit = [9])
    def post(self, user):
        return invoiceItemConfiguration.postRequest(user)
    """

@api.route('/'+invoiceItemConfiguration.path+'/<string:id>')
@api.doc(security = 'amivapitoken')
class InvoiceItemEndpointById(Resource):
    @authenticate()
    def get(self,id,user):
        return invoiceItemConfiguration.getRequestById(user,id)

    """
    @api.expect(invoiceItemConfiguration.model)
    @authenticate(requiredUserLevelBit = [9])
    def patch(self,id,user):
        return invoiceItemConfiguration.patchRequestById(user,id)
    """
