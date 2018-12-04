from flask_restplus import Namespace, Resource, fields

from sql import db
from sql.transactions import Invoice, InvoiceItem

from schemas.invoice import InvoiceSchema, InvoiceItemSchema

api = Namespace('Invoice', description='Invoice related operations.')

invoiceSchema = InvoiceSchema()
invoiceItemSchema = InvoiceItemSchema()

@api.route('/')
class Invoices(Resource):
    def get(self):
        query = db.session.query(Invoice)
        #apply user related filters
        res = []
        for result in query:
            temp = invoiceSchema.dump(result)[0]
            temp['number_of_items'] = len(result.items)
            res.append(temp)
        return res, 200

#Embeds items into invoice response
@api.route('/detail')
class InvoicesDetails(Resource):
    def get(self):
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
