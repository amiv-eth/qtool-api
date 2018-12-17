from flask_restplus import Namespace, Resource, fields
from flask import request

from .utility import authenticate, schemaToDict

from sql import db
from sql.transactions import Transaction,  DetailReceipt
from sql.transaction_util import TransactionAccount

from sqlalchemy import or_
from schemas.transaction import TransactionSchema, TransactionQuery, ReceiptSchema, TransactionEmbeddable
from schemas.query import QuerySchema, queryDocumentation

from requests.request import DatabaseRequest
from requests.transaction_access import TransactionAccess, ReceiptAccess
from requests.budget_access import BudgetItemAccess
from requests.query_parser import queryParser


api = Namespace('Transaction', description='Transaction related operations.')

transactionSchema = TransactionSchema()
transactionSchemaUser = TransactionSchema(exclude = ('account_id',))


receiptSchema = ReceiptSchema()


transaction_model = api.model('Transaction', schemaToDict(TransactionSchema))

transactionRequest = DatabaseRequest()
transactionRequest.databaseName = Transaction
transactionRequest.primaryKey = Transaction.id

"""
q = session.query(myClass)
for attr, value in web_dict.items():
    q = q.filter(getattr(myClass, attr).like("%%%s%%" % value))
"""

"""
testDocu = api.model('Docu', {
    'where': fields.Dictio(),
    'sort': fields.String(),
    'page': fields.String(),
    'embedded': fields.Dict()
})
"""

@api.route('/')
class Transactions(Resource):
    @api.doc(params=queryDocumentation, security='amivapitoken')
    @api.response(401, 'Unauthorized')
    @authenticate()
    def get(self,user):
        args = queryParser(Transaction, TransactionEmbeddable)
        """
        transactionAccessData = TransactionAccess(user)
        if 'embedded' in args:
            embeddedQuery = args.pop('embedded')
        else:
            embeddedQuery = {}
            for key in embeddedQuery:
                embeddedAccess[key] = embeddedQuery[key](user)
            print(embeddedAccess)
            res = transactionRequest.embedElement(transactionAccessData,embeddedAccess, **args)
        else:
            res = transactionRequest.getSerializedElements(transactionAccessData, **args)
        """
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
        transactionAccessData = TransactionAccess(user)
        receiptAccessData = ReceiptAccess(user)
        budgetItemAccess = BudgetItemAccess(user)
        res = transactionRequest.embedElement(transactionAccessData,{'receipt_data':receiptAccessData, 'budget_item':budgetItemAccess})
        return res
