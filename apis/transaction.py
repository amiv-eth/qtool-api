from flask_restplus import Namespace, Resource, fields
from flask import request

from .utility import authenticate

from sql import db
from sql.transactions import Transaction,  DetailReceipt
from sql.transaction_util import TransactionAccount

from sqlalchemy import or_
from schemas.transaction import TransactionSchema, TransactionQuery, ReceiptSchema

from requests.request import DatabaseRequest
from requests.transaction_access import TransactionAccess, ReceiptAccess
from requests.budget_access import BudgetItemAccess


api = Namespace('Transaction', description='Transaction related operations.')

transactionSchema = TransactionSchema()
transactionSchemaUser = TransactionSchema(exclude = ('account_id',))


receiptSchema = ReceiptSchema()

transaction_filters = {
	"comment": Transaction.comment,
    "user_id": Transaction.user_id,
    "description": Transaction.description,
    "type_id": Transaction.type_id,
    "budgetitem_id": Transaction.budgetitem_id,
    "currency_id": Transaction.currency_id,
    "amount": Transaction.amount,
    "is_valid": Transaction.is_valid,
    "financial_year": Transaction.financial_year,
    "date": Transaction.date,
    "category_id": Transaction.category_id,
    "id": Transaction.id,
    "account_id": Transaction.account_id
}

receipt_filters = {
	#Receipt Filters
	"receipt_received": DetailReceipt.receipt_received,
	"ezag_id": DetailReceipt.ezag_id,
	"bankstatement_period": DetailReceipt.bankstatement_period
}
receipt_filters.update(transaction_filters)




transactionParams = {}
for arg in transaction_filters:
	transactionParams[arg] = ""


receiptParams = {}
for arg in receipt_filters:
	receiptParams[arg] = ""


transaction_model = api.model('Transaction', {
    'financial_year': fields.Integer,
    'date': fields.DateTime,
    'type_id': fields.Integer,
    'description': fields.String,
    'category_id': fields.Integer,
    'budgetitem_id': fields.Integer,
    'account_id': fields.Integer,
    'is_valid': fields.Boolean,
    'amount': fields.Float,
    'currency_id': fields.Integer,
    'user_id': fields.Integer,
    'comment': fields.String
})

transactionRequest = DatabaseRequest()
transactionRequest.databaseName = Transaction
transactionRequest.primaryKey = Transaction.id



@api.route('/')
class Transactions(Resource):
    @api.doc(params=transactionParams, security='amivapitoken')
    @api.response(401, 'Unauthorized')
    @authenticate()
    def get(self,user):
        transactionAccessData = TransactionAccess(user)
        res = transactionRequest.getSerializedElements(transactionAccessData)
        return res, 200

    @api.doc(security='amivapitoken')
    @api.expect(transaction_model)
    @authenticate()
    def post(self,user):
        privileges = user.user_privileges
        if not (privileges>>9)&1:
            return {"message": "User not authorized."}, 401
        trans = transactionSchema.load(api.payload)[0]
        newTransaction = Transaction(
            financial_year=trans['financial_year'],
            date=trans['date'],
            type_id=trans['type_id'],
            description = trans['description'],
            category_id = trans['category_id'],
            budgetitem_id = trans['budgetitem_id'],
            account_id = trans['account_id'],
            is_valid = trans['is_valid'],
            amount = trans['amount'],
            currency_id = trans['currency_id'],
            user_id = trans['user_id'],
            comment = trans['comment']
        )
        db.session.add(newTransaction)
        db.session.commit()
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
        success = transactionRequest.patchElement(id, transactionAccessData, newData)
        if success:
            return {'message': 'Operation successful.'}, 202
        else:
            return {'message': 'Operation failed.'}, 500

    @api.doc(security = 'amivapitoken')
    @authenticate(requiredUserLevelBit = [9])
    def delete(self,id,user):
        transactionAccessData = TransactionAccess(user)
        transactionRequest.getElementById(id, transactionAccessData).is_valid = False
        db.session.commit()
        return {"message": "Operation successful."}, 202

@api.route('/receipt')
class Receipts(Resource):
    @api.doc(params=receiptParams, security = 'amivapitoken')
    @authenticate()
    def get(self,user):
        transactionAccessData = TransactionAccess(user)
        receiptAccessData = ReceiptAccess(user)
        budgetItemAccess = BudgetItemAccess(user)
        res = transactionRequest.embedElement(transactionAccessData,{'receipt_data':receiptAccessData, 'budget_item':budgetItemAccess})
        return res
