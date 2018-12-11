from schemas.transaction import TransactionSchema, ReceiptSchema
from sql.transactions import Transaction, DetailReceipt

from .access_control import AccessControl

from sqlalchemy import or_


class TransactionAccess(AccessControl):
    def specifyDatabase(self):
        self.databaseName = Transaction
        self.primaryKey = Transaction.id

    def applyUserLevelFilters(self, user):
        privileges = user.user_privileges
        if (privileges>>8)&1 or (privileges>>9)&1:
            return True
        if (privileges>>6)&1:
            filterExpression = (Transaction.user_id == user.user_id)
            for budget_item in user.own_budgetitem_id:
                filterExpression = or_(Transaction.budgetitem_id == budget_item.budgetitem_id, filterExpression)
            return filterExpression
        return (Transaction.user_id == user.user_id)

    def selectUserLevelSchema(self, user):
        transactionSchema = TransactionSchema()
        transactionSchemaUser = TransactionSchema(exclude = ('account_id',))
        privileges = user.user_privileges
        if (privileges>>8)&1 or (privileges>>9)&1:
            return transactionSchema
        return transactionSchemaUser


class ReceiptAccess(AccessControl):
    def specifyDatabase(self):
        self.databaseName = DetailReceipt
        self.primaryKey = DetailReceipt.transaction_id

    def applyUserLevelFilters(self,user):
        return True

    def selectUserLevelSchema(self, user):
        receiptSchema = ReceiptSchema()
        receiptSchemaUser = ReceiptSchema(exclude = ('ezag_id','bankstatement_period',))
        privileges = user.user_privileges
        if (privileges>>8)&1 or (privileges>>9)&1:
            return receiptSchema
        return receiptSchemaUser
