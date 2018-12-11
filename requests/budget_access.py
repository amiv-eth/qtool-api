from .access_control import AccessControl

from sql.budget import BudgetItem, BudgetConfirmed

from schemas.budget import BudgetItemSchema, BudgetConfirmedSchema


class BudgetItemAccess(AccessControl):
    def specifyDatabase(self):
        self.databaseName = BudgetItem
        self.primaryKey = BudgetItem.budgetitem_id

    def applyUserLevelFilters(self,user):
        return True

    def selectUserLevelSchema(self, user):
        return BudgetItemSchema()

class BudgetConfirmedAccess(AccessControl):
    def specifyDatabase(self):
        self.databaseName = BudgetConfirmed
        self.primaryKey = BudgetConfirmed.budgetitem_id

    def applyUserLevelFilters(self, user):
        return True

    def selectUserLevelSchema(self, user):
        return BudgetConfirmedSchema()
        