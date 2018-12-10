from .access_control import AccessControl

from sql.budget import BudgetItem

from schemas.budget import BudgetItemSchema


class BudgetItemAccess(AccessControl):
    def specifyDatabase(self):
        self.databaseName = BudgetItem
        self.primaryKey = BudgetItem.budgetitem_id

    def applyUserLevelFilters(self,user):
        return True

    def selectUserLevelSchema(self, user):
        return BudgetItemSchema()
        