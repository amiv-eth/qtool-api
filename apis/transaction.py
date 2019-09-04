from flask_restplus import Namespace, Resource

from sql import db

from schemas.transaction_utility import TransactionAccountSchema, TransactionCategorySchema, TransactionCurrencySchema, TransactionTypeSchema
import schemas.budget
import schemas.invoice
import schemas.people
import schemas.products
import schemas.transaction_utility
import schemas.transaction

from schemas.transaction import Transaction, TransactionSchema

from .query_parser import queryParser


api = Namespace('Transaction', description='Transaction related operations.')

queryDocumentation = {
    'where': "Filter criterion for database queries.",
    'sort': "Value by which the results are sorted by.",
    'page': "Number of the resultspage to display. Per page a maximum of 25 entries are displayed.",
    'embedded': "Toggle the embedding of additional ressources in the response."
}




@api.route('/transactions')
@api.doc(security = 'amivapitoken')
class TransactionEndpoint(Resource):
    @api.doc(params=queryDocumentation)
    def get(self):
        
        args = queryParser(Transaction, None)
        index = args["page"]
        print(args)
        transaction = Transaction.query.options(args["embedded"]).order_by(Transaction.transaction_id).offset(25*(index-1)).limit(25)
        transaction_dumped = TransactionSchema(many=True).dump(transaction)
        print(transaction_dumped.data)
        return (transaction_dumped.data,200)


"""
@api.route('/'+transactionConfiguration.path)
@api.doc(security = 'amivapitoken')
class TransactionEndpoint(Resource):
    @api.doc(params=queryDocumentation)
    @authenticate()
    def get(self,user):
        return transactionConfiguration.getRequest(user)
        
    @api.expect(transactionConfiguration.model)
    @authenticate(requiredUserLevelBit = [9])
    def post(self, user):
        return transactionConfiguration.postRequest(user)

@api.route('/'+transactionConfiguration.path+'/<string:id>')
@api.doc(security = 'amivapitoken')
class TransactionEndpointById(Resource):
    @authenticate()
    def get(self,id,user):
        return transactionConfiguration.getRequestById(user,id)

    @api.expect(transactionConfiguration.model)
    @authenticate(requiredUserLevelBit = [9])
    def patch(self,id,user):
        return transactionConfiguration.patchRequestById(user,id)

    @authenticate(requiredUserLevelBit = [9])
    def delete(self,id,user):
        transactionConfiguration.getElementById(id, user).is_valid = False
        db.session.commit()
        return {"message": "Operation successful."}, 202

# ToDo:
# - Automatically generate receipt entry for every expenditure transaction
receiptConfiguration = EndpointConfiguration(api, 'receipt', ReceiptAccess(), ReceiptEmbeddable())

@api.route('/'+receiptConfiguration.path)
class ReceiptEndpoint(Resource):
    @api.doc(params=queryDocumentation, security = 'amivapitoken')
    @authenticate()
    def get(self,user):
        return receiptConfiguration.getRequest(user)

@api.route('/'+receiptConfiguration.path+'/<string:id>')
@api.doc(security = 'amivapitoken')
class ReceiptEndpointById(Resource):
    @authenticate()
    def get(self,id,user):
        return receiptConfiguration.getRequestById(user,id)

    @api.expect(receiptConfiguration.model)
    @authenticate(requiredUserLevelBit = [9])
    def patch(self,id,user):
        return receiptConfiguration.patchRequestById(user,id)

"""