from marshmallow import Schema, fields

class AmivapiSessionSchema(Schema):
    user = fields.Str()
    token = fields.Str()

class AmivapiUserSchema(Schema):
    _id = fields.Str()
    nethz = fields.Str()
    firstname = fields.Str()
    lastname = fields.Str()
    membership = fields.Str()
    legi = fields.Int()
    department = fields.Str()
    gender = fields.Str()
    email = fields.Email()
    rfid = fields.Int()
    phone = fields.Str()
