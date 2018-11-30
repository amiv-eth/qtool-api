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
        return res

@api.route('/detail')
class InvoicesDetails(Resource):
    def get(self):
        query = db.session.query(Invoice)
        #apply user related filters
        res = []
        for result in query:
            temp = invoiceSchema.dump(result)[0]
            temp['number_of_items'] = len(result.items)
            for idx, item in enumerate(result.items):
                temp['item_'+str(idx+1)] = invoiceItemSchema.dump(item)[0]
            res.append(temp)
        return res
