from marshmallow_sqlalchemy import ModelSchema
from sql.transactions import Transaction, DetailReceipt
from sql.transactions import DetailMerchandise, Ezag

class TransactionSchema(ModelSchema):
    class Meta:
        model = Transaction

class ReceiptSchema(ModelSchema):
    class Meta:
        model = DetailReceipt

class MerchandiseSchema(ModelSchema):
    class Meta:
        model = DetailMerchandise

class EzagSchema(ModelSchema):
    class Meta:
        model = Ezag
