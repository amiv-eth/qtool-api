from sql import db
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy import ForeignKey
import datetime

#ToDo: Add field amount_chf to work with foreign currencies and fluctuating exchange rates
class Transaction(db.Model):
	id = db.Column(db.Integer, nullable=False, primary_key=True)
	financial_year = db.Column(INTEGER(4), nullable = False)
	date = db.Column(db.DateTime, default = datetime.datetime.now, nullable= False)
	type_id = db.Column(db.Integer, ForeignKey('transaction_type.type_id'), nullable = False)
	description = db.Column(db.String(255), nullable=False)
	category_id = db.Column(db.Integer, ForeignKey('transaction_category.category'), nullable = True)
	budgetitem_id = db.Column(db.Integer, ForeignKey('budget_item.budgetitem_id'), nullable= True)
	account_id = db.Column(db.Integer, ForeignKey('transaction_account.account'), nullable= True)
	is_valid = db.Column(db.Boolean, nullable= False) 
	amount = db.Column(db.Numeric(precision=10,scale=2), nullable = False, default=0.00)
	currency_id = db.Column(db.Integer, ForeignKey('transaction_currency.currency_id'), nullable= False)
	amount_in_chf = db.Column(db.Numeric(precision=10,scale=2), nullable = True)
	user_id = db.Column(db.Integer, ForeignKey('user.user_id'), nullable= False)
	comment = db.Column(db.String(255), nullable = True)

class DetailReceipt(db.Model):
	transaction_id = db.Column(db.Integer,ForeignKey('transaction.id'),nullable=False,  primary_key = True)
	receipt_received = db.Column(db.Boolean, nullable = False)
	ezag_id = db.Column(db.String(31), nullable = False)
	bankstatement_period = db.Column(db.String(31), nullable = False)


class DetailMerchandise(db.Model):
	transaction_id = db.Column(db.Integer, ForeignKey('transaction.id') ,nullable=False, primary_key = True)
	price = db.Column(db.Numeric(precision=6,scale=2), nullable = False, default=0.00)
	quantity = db.Column(INTEGER(6), nullable= False)
	article_id = db.Column(db.Integer, ForeignKey('merch_article.article_id'), nullable= False)

