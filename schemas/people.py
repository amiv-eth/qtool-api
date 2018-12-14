from marshmallow import Schema, fields
from sql import db
from sql.people import User, Customer

class CustomerSchema(Schema):
    customer_id = fields.Int(dump_only = True)
    category = fields.Str()
    company = fields.Str()
    title = fields.Str()
    first_name = fields.Str()
    last_name = fields.Str()
    address = fields.Str()
    plz = fields.Str()
    city = fields.Str()
    country = fields.Str()
    phone = fields.Str()
    email = fields.Email()
    quotation = fields.Str()

    def load_commit(self, data):
        desirialized = self.load(data)[0]
        element = Customer(**desirialized)
        db.session.add(element)
        db.session.commit()


class UserSchema(Schema):
    user_id = fields.Int(dump_only = True)
    nethz = fields.Str()
    password = fields.Str()
    salt = fields.Str()
    name = fields.Str()
    iban = fields.Str()
    bic = fields.Str()
    role = fields.Str()
    amiv_email = fields.Str()
    user_privileges = fields.Int()
    
    def load_commit(self, data):
        desirialized = self.load(data)[0]
        element = User(**desirialized)
        db.session.add(element)
        db.session.commit()