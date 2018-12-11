from marshmallow import Schema, fields, post_load
from sql.transaction_util import TransactionAccount, TransactionType, TransactionCategory, TransactionCurrency
from sql import db

class TransactionTypeSchema(Schema):
    type_id = fields.Int()
    type_class = fields.Str()
    type_name = fields.Str()

    @post_load
    def make_type(self, data):
        element = TransactionType(**data)
        db.session.add(element)
        db.session.commit()

class TransactionAccountSchema(Schema):
    account = fields.Int()
    account_name = fields.Str()

    @post_load
    def make_type(self, data):
        element = TransactionAccount(**data)
        db.session.add(element)
        db.session.commit()

class TransactionCategorySchema(Schema):
    category = fields.Int()
    category_name = fields.Str()

    @post_load
    def make_type(self, data):
        element = TransactionCategory(**data)
        db.session.add(element)
        db.session.commit()

class TransactionCurrencySchema(Schema):
    currency_id = fields.Int()
    currency_name = fields.Str()
    currency_shortcut = fields.Str()

    @post_load
    def make_type(self, data):
        element = TransactionCurrency(**data)
        db.session.add(element)
        db.session.commit()