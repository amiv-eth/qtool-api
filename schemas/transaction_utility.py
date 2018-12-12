from marshmallow import Schema, fields
from sql.transaction_util import TransactionAccount, TransactionType, TransactionCategory, TransactionCurrency
from sql import db

class TransactionTypeSchema(Schema):
    type_id = fields.Int()
    type_class = fields.Str()
    type_name = fields.Str()

    def load_commit(self, data):
        desirialized = self.load(data)[0]
        element = TransactionType(**desirialized)
        db.session.add(element)
        db.session.commit()

class TransactionAccountSchema(Schema):
    account = fields.Int()
    account_name = fields.Str()

    def load_commit(self, data):
        desirialized = self.load(data)[0]
        element = TransactionAccount(**desirialized)
        db.session.add(element)
        db.session.commit()

class TransactionCategorySchema(Schema):
    category = fields.Int()
    category_name = fields.Str()

    def load_commit(self, data):
        desirialized = self.load(data)[0]
        element = TransactionCategory(**desirialized)
        db.session.add(element)
        db.session.commit()

class TransactionCurrencySchema(Schema):
    currency_id = fields.Int()
    currency_name = fields.Str()
    currency_shortcut = fields.Str()

    def load_commit(self, data):
        desirialized = self.load(data)[0]
        element = TransactionCurrency(**desirialized)
        db.session.add(element)
        db.session.commit()