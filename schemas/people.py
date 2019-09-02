from marshmallow_sqlalchemy import ModelSchema
from sql.people import User, Customer

class UserSchema(ModelSchema):
    class Meta:
        model = User

class CustomerSchema(ModelSchema):
    class Meta:
        model = Customer
