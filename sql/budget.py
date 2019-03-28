from sql import db
from sqlalchemy.dialects.mysql import INTEGER

class BudgetItem(db.Model):
	budgetitem_id = db.Column(db.Integer, nullable = False, primary_key=True)
	budgetitem_code = db.Column(db.String(4), nullable = False)
	budgetgroup = db.Column(db.String(255), nullable = False)
	budgetitem_name = db.Column(db.String(255), nullable = False)
	financial_year = db.Column(INTEGER(4), nullable = False)
	expenditure_budgeted = db.Column(db.Numeric(precision=10,scale=2), nullable = False, default=0.00)
	revenue_budgeted = db.Column(db.Numeric(precision=10,scale=2), nullable = False, default=0.00)
	expenditure_confirmed = db.Column(db.Numeric(precision=10,scale=2), nullable = False, default=0.00)
	revenue_confirmed = db.Column(db.Numeric(precision=10,scale=2), nullable = False, default=0.00)


class Settings(db.Model):
	key = db.Column(db.String(63), nullable = False, primary_key=True)
	value = db.Column(db.String(255), nullable = False)

