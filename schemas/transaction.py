from marshmallow_sqlalchemy import ModelSchema
from sql.transactions import Transaction, DetailReceipt
from sql.transactions import DetailMerchandise, Ezag
from schemas import SmartNested


class TransactionSchema(ModelSchema):
    class Meta:
        model = Transaction

    financial_year = SmartNested("FinancialYearSchema", default=[], many=False)
    budgetitem = SmartNested("BudgetItemSchema", default=[], many=False)
    account = SmartNested("TransactionAccountSchema", default=[], many=False)
    category = SmartNested("TransactionCategorySchema", default=[], many=False)
    currency = SmartNested("TransactionCurrencySchema", default=[], many=False)
    type = SmartNested("TransactionTypeSchema", default=[], many=False)
    user = SmartNested("UserSchema", default=[], many=False)

class ReceiptSchema(ModelSchema):
    class Meta:
        model = DetailReceipt

class MerchandiseSchema(ModelSchema):
    class Meta:
        model = DetailMerchandise

class EzagSchema(ModelSchema):
    class Meta:
        model = Ezag
