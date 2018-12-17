from marshmallow import Schema, fields
from sql import db
from sql.transactions import Transaction
from schemas import EmbeddingSchema
from requests.utility_access import AccountAccess, CategoryAccess, CurrencyAccess, TypeAccess
from requests.budget_access import BudgetItemAccess
from requests.people_access import UserAccess
#Used to transform json to DB-Objects and vice-versa
class TransactionSchema(Schema):
	id = fields.Int(dump_only=True)
	financial_year = fields.Int()
	date = fields.DateTime()
	type_id = fields.Int()
	description = fields.Str()
	category_id = fields.Int()
	budgetitem_id = fields.Int()
	account_id = fields.Int()
	is_valid = fields.Bool()
	amount = fields.Float()
	currency_id = fields.Int()
	amount_in_chf = fields.Float()
	user_id = fields.Int()
	comment = fields.Str()

	def load_commit(self, data):
	    desirialized = self.load(data)[0]
	    element = Transaction(**desirialized)
	    db.session.add(element)
	    db.session.commit()

class TransactionEmbeddable(EmbeddingSchema):
	type = fields.Bool()
	category = fields.Bool()
	budgetitem = fields.Bool()
	account = fields.Bool()
	currency = fields.Bool()
	user = fields.Bool()

	accessData = {
		'type': TypeAccess,
		'category': CategoryAccess,
		'account': AccountAccess,
		'currency': CurrencyAccess,
		'budgetitem': BudgetItemAccess,
		'user': UserAccess
	}



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

