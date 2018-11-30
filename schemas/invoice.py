from marshmallow import Schema, fields

class InvoiceSchema(Schema):
    invoice_number = fields.Str()
    issue_date = fields.Date()
    ext_customer_db = fields.Bool()
    customer_id = fields.Int()
    duedate = fields.Date()
    moneyreceived = fields.Bool()
    reminderlevel = fields.Int()
    pdf_path = fields.Str()
    is_valid = fields.Bool()


class InvoiceItemSchema(Schema):
    transaction_id = fields.Int(dump_only=True)
    article_id = fields.Str()
    description = fields.Str()
    unit = fields.Str()
    amount = fields.Int()
    taxrate = fields.Float()
    unitprice = fields.Float()

    invoice_number = fields.String()
