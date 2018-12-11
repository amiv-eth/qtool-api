from schemas.invoice import InvoiceSchema, InvoiceItemSchema
from sql.invoice import Invoice, InvoiceItem

from .access_control import AccessControl


class InvoiceAccess(AccessControl):
    def specifyDatabase(self):
        self.databaseName = Invoice
        self.primaryKey = Invoice.invoice_id

    def applyUserLevelFilters(self, user):
        return True

    def selectUserLevelSchema(self, user):
        return InvoiceSchema()


class InvoiceItemAccess(AccessControl):
    def specifyDatabase(self):
        self.databaseName = InvoiceItem
        self.primaryKey = InvoiceItem.transaction_id

    def applyUserLevelFilters(self,user):
        return True

    def selectUserLevelSchema(self, user):
        return InvoiceItemSchema()
