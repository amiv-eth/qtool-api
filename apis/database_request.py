from flask_restplus import abort
from sql import db
from .query_parser import QueryParser


def loadPage(dbClass, dbSchema):
    query = QueryParser(dbClass).parseQueryFromRequest()
    embeddedQuery = dbClass.query.options(query.embedded)
    for relatedDatabase in query.join:
        embeddedQuery = embeddedQuery.outerjoin(relatedDatabase)
    orderedQuery = embeddedQuery.order_by(query.sort)
    filteredQuery = orderedQuery.filter(query.where)
    paginatedQuery = filteredQuery.offset(25*(query.page-1)).limit(25)
    dumpedQuery = dbSchema(many=True).dump(paginatedQuery).data
    return dumpedQuery

def loadEntry(dbClass, dbSchema, id=1):
    query = QueryParser().parseQueryFromRequest(dbClass)
    embeddedQuery = dbClass.query.options(query.embedded)
    oneElementQuery = embeddedQuery.get(id)
    if oneElementQuery == None:
        abort(400, 'Record with id ' +  id + ' does not exist.')
    dumpedQuery = dbSchema(many=False).dump(oneElementQuery).data
    return dumpedQuery

def postEntry(dbSchema,payload):
    element = dbSchema().load(payload)
    db.session.add(element)
    db.session.commit()
    return 200
