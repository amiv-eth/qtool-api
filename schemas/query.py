from marshmallow import Schema, fields

class QuerySchema(Schema):
    where = fields.Str()
    sort = fields.Str()
    page = fields.Int()
    embedded = fields.Str()


queryDocumentation = {
    'where': "Filter criterion for database queries.",
    'sort': "Value by which the results are sorted by.",
    'page': "Number of the resultspage to display. Per page a maximum of 25 entries are displayed.",
    'embedded': "Toggle the embedding of additional ressources in the response."
}