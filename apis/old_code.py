"""
merch_filters = {
    #Merch Filters
    "price": DetailMerchandise.price,
    "quantity": DetailMerchandise.quantity,
    "article_id": DetailMerchandise.article_id
}
merch_filters.update(transaction_filters)

merchParams = {}
for arg in merch_filters:
    merchParams[arg] = ""

@api.route('/merchandise')
class Merchandise(Resource):
    @api.doc(params=merchParams, security = 'amivapitoken')
    @authenticate
    def get(self,user):
        query = db.session.query(Transaction,DetailMerchandise).filter(DetailMerchandise.transaction_id == Transaction.id)
        query = applyUserFilters(query,user)
        query = applyQueryParams(query,"merchandise")
        response = []
        for result in query:
            transDict = transactionSchema.dump(result[0])[0]
            transDict.update(merchSchema.dump(result[1])[0])
            response.append(transDict)
        return response


"""