from requests import AccessControl

# Databases
from sql.budget import BudgetItem, BudgetConfirmed

# Schemas
from schemas.budget import BudgetItemSchema, BudgetConfirmedSchema


class BudgetItemAccess(AccessControl):
    def specifyDatabase(self):
        self.databaseName = BudgetItem
        self.databasePrimaryKey = BudgetItem.budgetitem_id
        self.schemaBase = BudgetItemSchema

    def getUserLevelFilters(self,user):
        return True

    def getUserLevelSchema(self, user):
        return BudgetItemSchema()

class BudgetConfirmedAccess(AccessControl):
    def specifyDatabase(self):
        self.databaseName = BudgetConfirmed
        self.databasePrimaryKey = BudgetConfirmed.budgetitem_id
        self.schemaBase = BudgetConfirmedSchema

    def getUserLevelFilters(self, user):
        return True

    def getUserLevelSchema(self, user):
        return BudgetConfirmedSchema()
        