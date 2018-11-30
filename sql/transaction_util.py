from sql import db
from sqlalchemy.dialects.mysql import INTEGER


class TransactionType(db.Model):
	type_id = db.Column(INTEGER(4), nullable= False, primary_key=True)
	type_class = db.Column(db.String(31), nullable= False)
	type_name = db.Column(db.String(31), nullable= False)

class TransactionAccount(db.Model):
	account = db.Column(db.String(4), nullable = False, primary_key=True)
	account_name = db.Column(db.String(255), nullable = False)

class TransactionCategory(db.Model):
	category = db.Column(INTEGER(4), nullable = False, primary_key=True)
	category_name = db.Column(db.String(255), nullable = False)

class TransactionCurrency(db.Model):
	currency_id = db.Column(INTEGER(4), nullable = False, primary_key=True)
	currency_name = db.Column(db.String(255), nullable = False)
	currency_shortcut = db.Column(db.String(3), nullable = False)

