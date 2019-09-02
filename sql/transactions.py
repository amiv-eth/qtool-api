from sql import db
from flask_sqlalchemy import ForeignKey
import datetime


class Transaction(db.Model):
    transaction_id = db.Column(db.Integer, nullable=False, primary_key=True)
    financial_year = financial_year = db.Column(db.Integer, ForeignKey('financial_year.financial_year_id'), nullable = False)
    date = db.Column(db.DateTime, default = datetime.datetime.now, nullable= False)
    type_id = db.Column(db.Integer, ForeignKey('transaction_type.type_id'), nullable = False)
    description = db.Column(db.String(255), nullable=False)
    category_id = db.Column(db.Integer, ForeignKey('transaction_category.category_id'), nullable = True)
    budgetitem_id = db.Column(db.Integer, ForeignKey('budget_item.budgetitem_id'), nullable= True)
    account_id = db.Column(db.Integer, ForeignKey('transaction_account.account_id'), nullable= True)
    is_valid = db.Column(db.Boolean, nullable= False) 
    amount = db.Column(db.Numeric(precision=10,scale=2), nullable = False, default=0.00)
    currency_id = db.Column(db.Integer, ForeignKey('transaction_currency.currency_id'), nullable= False)
    amount_in_chf = db.Column(db.Numeric(precision=10,scale=2), nullable = True)
    user_id = db.Column(db.Integer, ForeignKey('user.user_id'), nullable= False)
    comment = db.Column(db.String(255), nullable = True)


class DetailReceipt(db.Model):
    receipt_id = db.Column(db.Integer, nullable=False, primary_key=True)
    transaction_id = db.Column(db.Integer,ForeignKey('transaction.transaction_id'),nullable=False)
    receipt_received = db.Column(db.Boolean, nullable = False)
    ezag_id = db.Column(db.Integer,ForeignKey('ezag.ezag_id'),nullable=False)
    bankstatement_period = db.Column(db.String(31), nullable = False)
    custom_iban = db.Column(db.String(255), nullable = True)
    custom_recipient = db.Column(db.String(255), nullable = True)


class DetailMerchandise(db.Model):
    merchandise_id = db.Column(db.Integer, nullable=False, primary_key=True)
    transaction_id = db.Column(db.Integer, ForeignKey('transaction.transaction_id') ,nullable=False, primary_key = False)
    price = db.Column(db.Numeric(precision=6,scale=2), nullable = False, default=0.00)
    quantity = db.Column(db.Integer, nullable= False)
    article_id = db.Column(db.Integer, ForeignKey('merch_article.article_id'), nullable= False)


class Ezag(db.Model):
    ezag_id = db.Column(db.Integer, nullable=False, primary_key=True)
    ezag_name = db.Column(db.String(31), nullable = False) 