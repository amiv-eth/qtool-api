from marshmallow import Schema, fields
from sql.budget import BudgetItem
from sql import db

class BudgetItemSchema(Schema):
    budgetitem_id = fields.Int(dump_only = True)
    budgetitem_code = fields.Str()
    budgetgroup = fields.Str()
    budgetitem_name = fields.Str()
    financial_year = fields.Int()
    expenditure_budgeted = fields.Float()
    revenue_budgeted = fields.Float()

    def load_commit(self, data):
        desirialized = self.load(data)[0]
        element = BudgetItem(**desirialized)
        db.session.add(element)
        db.session.commit()

class BudgetConfirmedSchema(Schema):
    budgetitem_id = fields.Int(dump_only = True)
    financial_year = fields.Int()
    expenditure_effective = fields.Float()
    revenue_effective = fields.Float()