from marshmallow import Schema, fields

class BudgetItemSchema(Schema):
    budgetitem_id = fields.Str()
    budgetgroup = fields.Str()
    budgetitem_name = fields.Str()
    financial_year = fields.Int()
    expenditure_budgeted = fields.Float()
    revenue_budgeted = fields.Float()

class BudgetConfirmedSchema(Schema):
    budgetitem_id = fields.Str()
    financial_year = fields.Int()
    expenditure_effective = fields.Float()
    revenue_effective = fields.Float()