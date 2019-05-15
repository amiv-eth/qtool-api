from marshmallow import Schema, fields
from sql import db
from sql.invoice import Invoice, InvoiceItem

class InvoiceSchema(Schema):
    invoice_id = fields.Int(dump_only=True)
    invoice_number = fields.Str()
    issue_date = fields.Date()
    issuer_id = fields.Int()
    ext_customer_db = fields.Bool()
    customer_id = fields.Int()
    duedate = fields.Date()
    moneyreceived = fields.Bool()
    reminderlevel = fields.Int()
    pdf_path = fields.Str()
    is_valid = fields.Bool()

    def load_commit(self, data):
        desirialized = self.load(data)[0]
        element = Invoice(**desirialized)
        db.session.add(element)
        db.session.commit()


class InvoiceItemSchema(Schema):
    transaction_id = fields.Int(dump_only=True)
    article_id = fields.Str()
    description = fields.Str()
    unit = fields.Str()
    amount = fields.Int()
    taxrate = fields.Float()
    unitprice = fields.Float()

    invoice_id = fields.String()

    def load_commit(self, data):
        desirialized = self.load(data)[0]
        element = InvoiceItem(**desirialized)
        db.session.add(element)
        db.session.commit()