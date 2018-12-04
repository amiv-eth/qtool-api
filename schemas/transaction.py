from marshmallow import Schema, fields
#Used to transform json to DB-Objects and vice-versa
class TransactionSchema(Schema):
	id = fields.Int(dump_only=True)
	financial_year = fields.Int()
	date = fields.DateTime()
	type_id = fields.Int()
	description = fields.Str()
	category_id = fields.Int()
	budgetitem_id = fields.Str()
	account_id = fields.Str()
	is_valid = fields.Bool()
	amount = fields.Float()
	currency_id = fields.Int()
	amount_in_chf = fields.Float()
	user_id = fields.Int()
	comment = fields.Str()



class TransactionQuery(TransactionSchema):
	id = fields.Int(dump_only=False)
	pass

class ReceiptSchema(Schema):
	transaction_id = fields.Int(dump_only=True)
	receipt_received = fields.Bool()
	ezag_id = fields.Str()
	bankstatement_period = fields.Str()

class MerchSchema(Schema):
	transaction_id = fields.Int(dump_only=True)
	price = fields.Float()
	quantity = fields.Int()
	article_id = fields.Int()

