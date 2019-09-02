from marshmallow_sqlalchemy import ModelSchema
from sql.budget import BudgetItem, BudgetGroup, FinancialYear

class BudgetItemSchema(ModelSchema):
    class Meta:
        model = BudgetItem

class BudgetGroupSchema(ModelSchema):
    class Meta:
        model = BudgetGroup

class FinancialYearSchema(ModelSchema):
    class Meta:
        model = FinancialYear