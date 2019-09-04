from .query_parser import queryParser


def loadPage(dbClass, dbSchema):
    args = queryParser(dbClass)
    index = args["page"]
    embeddedQuery = dbClass.query.options(args["embedded"])
    orderedQuery = embeddedQuery.order_by(args["sort"])
    filteredQuery = orderedQuery.filter(args["where"])
    paginatedQuery = filteredQuery.offset(25*(index-1)).limit(25)
    dumpedQuery = dbSchema(many=True).dump(paginatedQuery).data
    return dumpedQuery