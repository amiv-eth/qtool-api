from marshmallow_sqlalchemy import ModelSchema
from sql.products import InvoiceArticle, MerchArticle

class InvoiceArticleSchema(ModelSchema):
    class Meta:
        model = InvoiceArticle

class MerchArticleSchema(ModelSchema):
    class Meta:
        model = MerchArticle