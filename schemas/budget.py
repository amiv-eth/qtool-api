from marshmallow import Schema, fields
from sql.budget import BudgetItem, BudgetGroup
from sql import db

class BudgetItemSchema(Schema):
    budgetitem_id = fields.Int(dump_only = True)
    budgetitem_code = fields.Str()
    budgetgroup_id = fields.Str()
    budgetitem_name = fields.Str()
    financial_year = fields.Int()
    expenditure_budgeted = fields.Float()
    revenue_budgeted = fields.Float()
    expenditure_confirmed = fields.Float()
    revenue_confirmed = fields.Float()

    def load_commit(self, data):
        desirialized = self.load(data)[0]
        element = BudgetItem(**desirialized)
        db.session.add(element)
        db.session.commit()
        return element

class BudgetGroupSchema(Schema):
    budgetgroup_id = fields.Int()
    budgetgroup_name = fields.Str()

    def load_commit(self, data):
        desirialized = self.load(data)[0]
        element = BudgetGroup(**desirialized)
        db.session.add(element)
        db.session.commit()
