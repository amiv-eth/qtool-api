from flask_restplus import Namespace, Resource

from .utility import authenticate, queryDocumentation

from sql import db
from sql.invoice import Invoice, InvoiceItem

from schemas.invoice import InvoiceSchema, InvoiceItemSchema

from apis.query_parser import queryParser
from apis.template import EndpointConfiguration
from access.invoice_access import InvoiceAccess, InvoiceEmbeddable

api = Namespace('Invoice', description='Invoice related operations.')
"""
dbRequest = EndpointConfiguration()

invoiceSchema = InvoiceSchema()
invoiceItemSchema = InvoiceItemSchema()

@api.route('/')
class Invoices(Resource):
    @api.doc(params = queryDocumentation, security='amivapitoken')
    @authenticate(requiredUserLevelBit = [7,8,9])
    def get(self,user):
        args = queryParser(Invoice, InvoiceEmbeddable)
        res = dbRequest.getSerializedResponse(user, InvoiceAccess, **args)
        return res, 200


#Embeds items into invoice response
@api.route('/detail')
class InvoicesDetails(Resource):
    @api.doc(security='amivapitoken')
    @authenticate(requiredUserLevelBit = [7,8,9])
    def get(self,user):
        # Edge case, need to embed multiple items! 
        query = db.session.query(Invoice)
        #apply user related filters
        res = []
        for result in query:
            temp = invoiceSchema.dump(result)[0]
            temp['number_of_items'] = len(result.items)
            temp['items'] = [invoiceItemSchema.dump(item)[0] for item in result.items]
            res.append(temp)
        return res, 200

@api.route('/item/<string:id>')
class InvoiceItems(Resource):
    def get(self, id):
        query = db.session.query(InvoiceItem).filter(InvoiceItem.transaction_id == id)
        if not query.first():
            return {'message': 'Id does not exist!'}, 404 
        res = invoiceItemSchema.dump(query.first())[0]
        return res, 200
"""