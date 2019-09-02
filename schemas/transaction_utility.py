from marshmallow_sqlalchemy import ModelSchema
from sql.transaction_utility import TransactionAccount, TransactionCategory
from sql.transaction_utility import TransactionCurrency, TransactionType

class TransactionAccountSchema(ModelSchema):
    class Meta:
        model = TransactionAccount

class TransactionCategorySchema(ModelSchema):
    class Meta:
        model = TransactionCategory

class TransactionCurrencySchema(ModelSchema):
    class Meta:
        model = TransactionCurrency

class TransactionTypeSchema(ModelSchema):
    class Meta:
        model = TransactionType
