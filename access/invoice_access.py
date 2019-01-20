from access import AccessControl, EmbeddingSchema
from marshmallow import fields

# Databases
from sql.invoice import Invoice, InvoiceItem

# Schemas
from schemas.invoice import InvoiceSchema, InvoiceItemSchema

# Embedding
from access.people_access import UserAccess, CustomerAccess


class InvoiceAccess(AccessControl):
    def specifyDatabase(self):
        self.databaseName = Invoice
        self.databasePrimaryKey = Invoice.invoice_id
        self.schemaBase = InvoiceSchema

    def getUserLevelFilters(self, user):
        return True

    def getUserLevelSchema(self, user):
        return InvoiceSchema()


class InvoiceItemAccess(AccessControl):
    def specifyDatabase(self):
        self.databaseName = InvoiceItem
        self.databasePrimaryKey = InvoiceItem.transaction_id
        self.schemaBase = InvoiceItemSchema

    def getUserLevelFilters(self,user):
        return True

    def getUserLevelSchema(self, user):
        return InvoiceItemSchema()

class InvoiceEmbeddable(EmbeddingSchema):
    user = fields.Bool()
    customer = fields.Bool()

    accessData = {
        'user': UserAccess,
        'customer': CustomerAccess
    }
