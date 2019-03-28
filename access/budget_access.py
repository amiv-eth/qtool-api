from access import AccessControl

# Databases
from sql.budget import BudgetItem

# Schemas
from schemas.budget import BudgetItemSchema


class BudgetItemAccess(AccessControl):
    def specifyDatabase(self):
        self.databaseName = BudgetItem
        self.databasePrimaryKey = BudgetItem.budgetitem_id
        self.schemaBase = BudgetItemSchema

    def getUserLevelFilters(self,user):
        return True

    def getUserLevelSchema(self, user):
        return BudgetItemSchema()
