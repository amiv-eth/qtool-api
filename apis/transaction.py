from flask_restplus import Namespace, Resource

from .utility import authenticate, schemaToDict, queryDocumentation

from sql import db
from sql.transactions import Transaction, DetailReceipt

from schemas.transaction import TransactionSchema, ReceiptSchema

from requests.request import DatabaseRequest
from requests.transaction_access import TransactionAccess, ReceiptAccess, TransactionEmbeddable, ReceiptEmbeddable
from requests.query_parser import queryParser


api = Namespace('Transaction', description='Transaction related operations.')

transactionSchema = TransactionSchema()
transactionSchemaUser = TransactionSchema(exclude = ('account_id',))


receiptSchema = ReceiptSchema()


transaction_model = api.model('Transaction', schemaToDict(TransactionSchema))

transactionRequest = DatabaseRequest()
transactionRequest.databaseName = Transaction
transactionRequest.primaryKey = Transaction.id



@api.route('/')
class Transactions(Resource):
    @api.doc(params=queryDocumentation, security='amivapitoken')
    @api.response(401, 'Unauthorized')
    @authenticate()
    def get(self,user):
        args = queryParser(Transaction, TransactionEmbeddable)
        res = transactionRequest.getSerializedResponse(user, TransactionAccess, **args)
        return res, 200

    @api.doc(security='amivapitoken')
    @api.expect(transaction_model)
    @authenticate(requiredUserLevelBit = [9])
    def post(self,user):
        transactionSchema.load_commit(api.payload)
        return {'result': 'Transaction added.'}, 201

	
@api.route('/<string:id>')
class ReceiptById(Resource):
    @api.doc(security = 'amivapitoken')
    @authenticate()
    def get(self, id, user):
        transactionAccessData = TransactionAccess(user)
        return transactionRequest.getSerializedElementById(id,transactionAccessData)

    @api.expect(transaction_model)
    @api.doc(security = 'amivapitoken')
    @authenticate(requiredUserLevelBit = [9])
    def patch(self, id, user):
        transactionAccessData = TransactionAccess(user)
        newData = transactionSchema.load(api.payload)[0]
        return transactionRequest.patchElement(id, transactionAccessData, newData)

    @api.doc(security = 'amivapitoken')
    @authenticate(requiredUserLevelBit = [9])
    def delete(self,id,user):
        transactionAccessData = TransactionAccess(user)
        transactionRequest.getElementById(id, transactionAccessData).is_valid = False
        db.session.commit()
        return {"message": "Operation successful."}, 202


@api.route('/receipt')
class Receipts(Resource):
    @api.doc(params=queryDocumentation, security = 'amivapitoken')
    @authenticate()
    def get(self,user):
        args = queryParser(DetailReceipt, ReceiptEmbeddable)
        res = transactionRequest.getSerializedResponse(user, ReceiptAccess, **args)
        return res, 200
        """
        transactionAccessData = TransactionAccess(user)
        receiptAccessData = ReceiptAccess(user)
        budgetItemAccess = BudgetItemAccess(user)
        res = transactionRequest.embedElement(transactionAccessData,{'receipt_data':receiptAccessData, 'budget_item':budgetItemAccess})
        return res
        """
