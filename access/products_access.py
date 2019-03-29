from access import AccessControl

# Databases
from sql.products import InvoiceArticle

# Schemas
from schemas.products import InvoiceArticleSchema


class InvoiceArticleAccess(AccessControl):
    def specifyDatabase(self):
        self.databaseName = InvoiceArticle
        self.databasePrimaryKey = InvoiceArticle.article_id
        self.schemaBase = InvoiceArticleSchema

    def getUserLevelFilters(self,user):
        return True

    def getUserLevelSchema(self, user):
        return InvoiceArticleSchema()