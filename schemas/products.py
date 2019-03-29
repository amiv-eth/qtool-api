from marshmallow import Schema, fields
from sql import db
from sql.products import InvoiceArticle


class InvoiceArticleSchema(Schema):
    article_id = fields.Int(dump_only=True)
    article_code = fields.Str()
    article = fields.Str()
    description = fields.Str()
    unit = fields.Str()
    budgetitem_id = fields.Int()
    productgroup = fields.Str()
    mwst = fields.Float()
    unitprice = fields.Float()

    def load_commit(self, data):
        desirialized = self.load(data)[0]
        element = InvoiceArticle(**desirialized)
        db.session.add(element)
        db.session.commit()