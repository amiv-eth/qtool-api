from access import AccessControl, EmbeddingSchema
from marshmallow import fields

# Databases
from sql.budget import BudgetItem, BudgetGroup

# Schemas
from schemas.budget import BudgetItemSchema, BudgetGroupSchema


class BudgetItemAccess(AccessControl):
    def specifyDatabase(self):
        self.databaseName = BudgetItem
        self.databasePrimaryKey = BudgetItem.budgetitem_id
        self.schemaBase = BudgetItemSchema

    def getUserLevelFilters(self,user):
        return True

    def getUserLevelSchema(self, user):
        return BudgetItemSchema()

class BudgetGroupAccess(AccessControl):
    def specifyDatabase(self):
        self.databaseName = BudgetGroup
        self.databasePrimaryKey = BudgetGroup.budgetgroup_id
        self.schemaBase = BudgetGroupSchema

    def getUserLevelFilters(self, user):
        return True

    def getUserLevelSchema(self, user):
        return BudgetGroupSchema()

class BudgetItemEmbeddable(EmbeddingSchema):
    budgetgroup = fields.Bool()
    
    accessData = {
        'budgetgroup': BudgetGroupAccess
    }