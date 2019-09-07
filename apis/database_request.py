from .query_parser import QueryParser


def loadPage(dbClass, dbSchema):
    query = QueryParser().parseQueryFromRequest(dbClass)
    embeddedQuery = dbClass.query.options(query.embedded)#.outerjoin(primaryDatabase)
    for relatedDatabase in query.join:
        embeddedQuery = embeddedQuery.outerjoin(relatedDatabase)
    orderedQuery = embeddedQuery.order_by(query.sort)
    filteredQuery = orderedQuery.filter(query.where)
    paginatedQuery = filteredQuery.offset(25*(query.page-1)).limit(25)
    dumpedQuery = dbSchema(many=True).dump(paginatedQuery).data
    return dumpedQuery