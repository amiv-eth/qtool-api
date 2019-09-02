from sql import db, BaseModel


class BudgetItem(BaseModel):
    budgetitem_id = db.Column(db.Integer, nullable = False, primary_key=True)
    budgetitem_code = db.Column(db.String(4), nullable = False)
    budgetgroup_id = db.Column(db.Integer, db.ForeignKey('budget_group.budgetgroup_id'), nullable = False)
    budgetitem_name = db.Column(db.String(255), nullable = False)
    financial_year_id = db.Column(db.Integer, db.ForeignKey('financial_year.financial_year_id'), nullable = True)
    expenditure_budgeted = db.Column(db.Numeric(precision=10,scale=2), nullable = False, default=0.00)
    revenue_budgeted = db.Column(db.Numeric(precision=10,scale=2), nullable = False, default=0.00)
    expenditure_confirmed = db.Column(db.Numeric(precision=10,scale=2), nullable = False, default=0.00)
    revenue_confirmed = db.Column(db.Numeric(precision=10,scale=2), nullable = False, default=0.00)


class BudgetGroup(BaseModel):
    budgetgroup_id = db.Column(db.Integer, nullable = False, primary_key=True)
    budgetgroup_name = db.Column(db.String(255), nullable = False)


class FinancialYear(BaseModel):
    financial_year_id = db.Column(db.Integer, nullable = False, primary_key=True)
    financial_year = db.Column(db.Integer, nullable = False, primary_key=False)


class Settings(BaseModel):
    key = db.Column(db.String(63), nullable = False, primary_key=True)
    value = db.Column(db.String(255), nullable = False)

