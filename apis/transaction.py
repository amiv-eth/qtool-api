from flask_restplus import Namespace, Resource, fields
from flask import request

from .utility import authenticate, checkForExistence

from sql import db
from sql.transactions import Transaction,  DetailReceipt
from sql.transaction_util import TransactionAccount

from sqlalchemy import or_
from schemas.transaction import TransactionSchema, TransactionQuery, ReceiptSchema

from queries.request import DatabaseRequest


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
    'budgetitem_id': fields.String,
    'account_id': fields.String,
    'is_valid': fields.Boolean,
    'amount': fields.Integer,
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
        userLevelFilters = applyUserLevelFilters(user)
        userLevelSchema = selectUserLevelSchema(user)
        res = transactionRequest.getSerializedElements(schema=userLevelSchema,userLevelFilters=userLevelFilters)
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
        userLevelFilters = applyUserLevelFilters(user)
        userLevelSchema = selectUserLevelSchema(user)
        return transactionRequest.getSerializedElementById(id,userLevelSchema,userLevelFilters)

    @api.expect(transaction_model)
    @api.doc(security = 'amivapitoken')
    @authenticate(requireUserLevelBit = 9)
    def patch(self, id, user):
        query = db.session.query(Transaction).filter(Transaction.id == id)
        if not query.first():
            return {'message': 'Id does not exist!'}, 404
        element = query.first()
        newData = transactionSchema.load(api.payload)[0]
        for key in newData:
            setattr(element, key, newData[key])
        db.session.commit()
        return {'message': 'Operation successful.'}, 202

    @api.doc(security = 'amivapitoken')
    @authenticate(requireUserLevelBit = 9)
    def delete(self,id,user):
        query = db.session.query(Transaction).filter(Transaction.id == id)
        if not query.first():
            return {'message': 'Id does not exist!'}, 404
        query.first().is_valid = False
        db.session.commit()
        return {"message": "Operation successful."}, 202

@api.route('/receipt')
class Receipts(Resource):
	@api.doc(params=receiptParams, security = 'amivapitoken')
	@authenticate()
	def get(self,user):
		query = db.session.query(Transaction,DetailReceipt).filter(DetailReceipt.transaction_id == Transaction.id)
		query = applyUserFilters(query,user)
		query = applyQueryParams(query,"receipt")
		response = []
		for result in query:
			transDict = transactionSchema.dump(result[0])[0]
			transDict.update(receiptSchema.dump(result[1])[0])
			response.append(transDict)
		return response



		
def applyQueryParams(query,detail="none"):
	#Get query parameters
	requ = request.args.to_dict(flat=True)
	#Validate query parameter
	qSchema = TransactionQuery()
	parameters = qSchema.load(requ)[0]
	if detail == "receipt":
		parameters.update(receiptSchema.load(requ)[0])
		filters=receipt_filters
	else:
		filters=transaction_filters
	#err = qSchema.load(requ)[1]
	#Generate DB query according to the get request parameters
	for key in parameters:
		if arg == "description" or arg == "comment":
			query = query.filter(filters[key].contains(parameters[key]))
		else:
			query = query.filter(filters[key] == parameters[key])

	return query

def applyUserFilters(query,user):
	privileges = user.user_privileges
	if (privileges>>8)&1 or (privileges>>9)&1:
		return query
	if (privileges>>6)&1:
		return query.filter(or_(Transaction.budgetitem_id == "303K", Transaction.user_id == user.user_id))
	return query.filter(Transaction.user_id == user.user_id)

def applyUserLevelFilters(user):
        privileges = user.user_privileges
        if (privileges>>8)&1 or (privileges>>9)&1:
            return True
        if (privileges>>6)&1:
            return (or_(Transaction.budgetitem_id == "303K", Transaction.user_id == user.user_id))
        return (Transaction.user_id == user.user_id)

def selectUserLevelSchema(user):
    privileges = user.user_privileges
    if (privileges>>8)&1 or (privileges>>9)&1:
        return transactionSchema
    return transactionSchemaUser





