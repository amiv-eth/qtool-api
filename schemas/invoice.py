from marshmallow import Schema, fields
from flask_marshmallow import Marshmallow
from sql import db
from sql.invoice import Invoice, InvoiceItem

from sql.transactions import Transaction
from sql.people import User

ma = Marshmallow()

class SmartNested(fields.Nested):
    def serialize(self, attr, obj, accessor=None):
        if attr not in obj.__dict__:
            return int(getattr(obj, attr + "_id"))
        return super(SmartNested, self).serialize(attr, obj, accessor)

class InvoiceSchema(ma.ModelSchema):
    class Meta:
        model = Invoice
        sqla_session = db.session
        include_fk = True

    itemsContent = fields.Nested('InvoiceItemSchema', default=[], many=True, exclude=('invoice',), attribute='items')
    issuer = SmartNested('UserSchema2', default=[], many=False)
    

class InvoiceItemSchema(ma.ModelSchema):
    class Meta:
        model = InvoiceItem
        sqla_session = db.session
        include_fk = True

    invoice = fields.Nested('InvoiceSchema', default=[], many=False, exclude=('items','itemsContent'))
    transaction_id = fields.Nested('TransactionSchema2',default=[],many=False)

class TransactionSchema2(ma.ModelSchema):
    class Meta:
        model = Transaction
        sqla_session = db.session
        include_fk = True

class UserSchema2(ma.ModelSchema):
    class Meta:
        model = User
        sqla_session = db.session
        include_fk = True


"""
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
"""