from .access_control import AccessControl

# Databases
from sql.transaction_util import TransactionAccount, TransactionCategory, TransactionCurrency, TransactionType

# Schemas
from schemas.transaction_utility import TransactionAccountSchema, TransactionCategorySchema, TransactionCurrencySchema, TransactionTypeSchema


class AccountAccess(AccessControl):
    def specifyDatabase(self):
        self.databaseName = TransactionAccount
        self.databasePrimaryKey = TransactionAccount.account
        self.schemaBase = TransactionAccountSchema

    def getUserLevelFilters(self,user):
        return True

    def getUserLevelSchema(self, user):
        return TransactionAccountSchema()

class CategoryAccess(AccessControl):
    def specifyDatabase(self):
        self.databaseName = TransactionCategory
        self.databasePrimaryKey = TransactionCategory.category
        self.schemaBase = TransactionCategorySchema
        
    def getUserLevelFilters(self, user):
        return True

    def getUserLevelSchema(self, user):
        return TransactionCategorySchema()

class CurrencyAccess(AccessControl):
    def specifyDatabase(self):
        self.databaseName = TransactionCurrency
        self.databasePrimaryKey = TransactionCurrency.currency_id
        self.schemaBase = TransactionCurrencySchema
        
    def getUserLevelFilters(self, user):
        return True

    def getUserLevelSchema(self, user):
        return TransactionCurrencySchema()

class TypeAccess(AccessControl):
    def specifyDatabase(self):
        self.databaseName = TransactionType
        self.databasePrimaryKey = TransactionType.type_id
        self.schemaBase = TransactionTypeSchema

    def getUserLevelFilters(self, user):
        return True

    def getUserLevelSchema(self, user):
        return TransactionTypeSchema()