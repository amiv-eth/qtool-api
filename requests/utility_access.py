from .access_control import AccessControl

from sql.transaction_util import TransactionAccount, TransactionCategory, TransactionCurrency, TransactionType

from schemas.transaction_utility import TransactionAccountSchema, TransactionCategorySchema, TransactionCurrencySchema, TransactionTypeSchema


class AccountAccess(AccessControl):
    def specifyDatabase(self):
        self.databaseName = TransactionAccount
        self.primaryKey = TransactionAccount.account
        self.baseSchema = TransactionAccountSchema

    def applyUserLevelFilters(self,user):
        return True

    def selectUserLevelSchema(self, user):
        return TransactionAccountSchema()

class CategoryAccess(AccessControl):
    def specifyDatabase(self):
        self.databaseName = TransactionCategory
        self.primaryKey = TransactionCategory.category
        self.baseSchema = TransactionCategorySchema

    def applyUserLevelFilters(self, user):
        return True

    def selectUserLevelSchema(self, user):
        return TransactionCategorySchema()

class CurrencyAccess(AccessControl):
    def specifyDatabase(self):
        self.databaseName = TransactionCurrency
        self.primaryKey = TransactionCurrency.currency_id
        self.baseSchema = TransactionCurrencySchema

    def applyUserLevelFilters(self, user):
        return True

    def selectUserLevelSchema(self, user):
        return TransactionCurrencySchema()

class TypeAccess(AccessControl):
    def specifyDatabase(self):
        self.databaseName = TransactionType
        self.primaryKey = TransactionType.type_id
        self.baseSchema = TransactionTypeSchema

    def applyUserLevelFilters(self, user):
        return True

    def selectUserLevelSchema(self, user):
        return TransactionTypeSchema()