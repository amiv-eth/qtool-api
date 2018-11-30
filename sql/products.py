from sql import db


class InvoiceArticle(db.Model):
	article_id = db.Column(db.String(255), nullable = False, primary_key=True)
	article = db.Column(db.String(255), nullable=False)
	description = db.Column(db.String(255), nullable=False)
	unit = db.Column(db.String(255), nullable=False)
	budgetitem_id = db.Column(db.String(4), nullable = False)
	productgroup = db.Column(db.String(255), nullable=False)
	mwst = db.Column(db.Numeric(precision=5,scale=2), nullable = False, default=0.00)
	unitprice = db.Column(db.Numeric(precision=8,scale=2), nullable = False, default=0.00)

class MerchArticle(db.Model):
	article_id = db.Column(db.Integer, nullable = False, primary_key=True)
	article = db.Column(db.String(255), nullable = False)
	unitprice = db.Column(db.Numeric(precision=6,scale=2), nullable = False, default=0.00)