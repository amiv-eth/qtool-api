from sql import db
from sqlalchemy import ForeignKey
import datetime

from .products import InvoiceArticle

class Invoice(db.Model):
    invoice_id = db.Column(db.Integer, nullable=False, primary_key=True)
    invoice_number = db.Column(db.String(7), nullable=False)
    issuer_id = db.Column(db.Integer, ForeignKey('user.user_id'), nullable= False)
    issue_date = db.Column(db.DATE, default = datetime.datetime.now, nullable= False)
    ext_customer_db = db.Column(db.Boolean, nullable=False)
    customer_id = db.Column(db.Integer, ForeignKey('customer.customer_id'), nullable=False)
    duedate = db.Column(db.DATE, default = datetime.datetime.now, nullable= False)
    moneyreceived = db.Column(db.Boolean, nullable=False)
    reminderlevel = db.Column(db.Integer, nullable=False)
    pdf_path = db.Column(db.String(255), nullable=False)
    is_valid = db.Column(db.Boolean, nullable= False)

    items = db.relationship('InvoiceItem', backref='invoice', lazy=True)
    issuer = db.relationship('User', lazy = True)
    customer = db.relationship('Customer', lazy = True)
    
class InvoiceItem(db.Model):
    transaction_id = db.Column(db.Integer, ForeignKey('transaction.id'), nullable=False, primary_key = True)
    article_id = db.Column(db.Integer, ForeignKey('invoice_article.article_id'),  nullable=False)
    description = db.Column(db.Text, nullable=False)
    unit = db.Column(db.String(7), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    taxrate = db.Column(db.Float(), nullable=False)
    unitprice = db.Column(db.Float(), nullable=False)
    invoice_id = db.Column(db.Integer, db.ForeignKey('invoice.invoice_id'),nullable=False)

    transaction = db.relationship('Transaction', lazy = True)
    article = db.relationship('InvoiceArticle', lazy = True)