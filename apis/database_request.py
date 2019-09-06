from .query_parser import queryParser


def loadPage(dbClass, dbSchema):
    args = queryParser(dbClass)
    index = args["page"]
    (sortBy,primaryDatabase) = args['sort']
    embeddedQuery = dbClass.query.options(args["embedded"]).outerjoin('user').outerjoin('account')#.outerjoin(primaryDatabase)
    orderedQuery = embeddedQuery.order_by(sortBy)
    filteredQuery = orderedQuery.filter(args["where"])
    print(filteredQuery.count())
    paginatedQuery = filteredQuery.offset(25*(index-1)).limit(25)
    dumpedQuery = dbSchema(many=True).dump(paginatedQuery).data
    return dumpedQuery