from flask_restplus import Namespace, Resource

from sql.budget import BudgetItem

from sql import db
from sql.transactions import Transaction

from .utility import authenticate, schemaToDict

from sqlalchemy import or_

from schemas.budget import BudgetConfirmedSchema, BudgetItemSchema

from access.budget_access import BudgetConfirmedAccess, BudgetItemAccess
from apis.template import EndpointConfiguration


api = Namespace('Budget', description='Budget related operations.')

budgetItemSchema = BudgetItemSchema()
budgetConfirmedSchema = BudgetConfirmedSchema()
"""
dbRequest = EndpointConfiguration()


path = 'items'
schema = BudgetItemSchema()
model = api.model(path.title(), schemaToDict(schema))
access = BudgetItemAccess

@api.route('/'+path)
class Item(Resource):
    @api.doc(security='amivapitoken')
    @authenticate()
    def get(self,user):
        res = dbRequest.getSerializedResponse(user,access)
        return res, 200

    @api.doc(security='amivapitoken')
    @api.expect(model)
    @authenticate(requiredUserLevelBit = [9])
    def post(self, user):
        schema.load_commit(api.payload)
        return {'result': path.title() + ' added.'}, 201

@api.route('/'+path+'/<string:id>')
class ItemById(Resource):
    @api.doc(security='amivapitoken')
    @authenticate()
    def get(self,id,user):
        accessData = access(user)
        return dbRequest.getSerializedElementById(id,accessData)

    @api.expect(model)
    @api.doc(security='amivapitoken')
    @authenticate(requiredUserLevelBit = [9])
    def patch(self,id,user):
        accessData = access(user)
        newData = schema.load(api.payload)[0]
        return dbRequest.patchElement(id,accessData,newData)

    @api.doc(security = 'amivapitoken')
    @authenticate(requiredUserLevelBit = [9])
    def delete(self,id,user):
        accessData = access(user)
        dbRequest.getElementById(id, accessData).financial_year = 0
        db.session.commit()
        return {"message": "Operation successful."}, 202



@api.route('/confirmed')
class BudgetConf(Resource):
    @api.doc(security='amivapitoken')
    @authenticate()
    def get(self,user):
        res = dbRequest.getSerializedResponse(user,BudgetConfirmedAccess)
        return res

@api.route('/calculated')
class BudgetCalculated(Resource):
    def get(self):
        #ToDo: Cache result
        values = calculateBudget()
        return values

#ToDo: Add amount in CHF for reasonable numbers!
#ToDo: Specify a financial_year
def calculateBudget():
    query = db.session.query(BudgetItem.budgetitem_id)
    response = []
    for result in query:
        budgetitem_id = result[0]
        budgetItemCalculated = {'budgetitem_id' : budgetitem_id}
        
        transactions = db.session.query(Transaction.amount).filter(Transaction.budgetitem_id == budgetitem_id).filter(Transaction.currency_id == 1)
        revenueTransactions = transactions.filter(or_(Transaction.type_id.startswith('1'),Transaction.type_id.startswith('3')))
        expenditureTransactions = transactions.filter(or_(Transaction.type_id.startswith('2'),Transaction.type_id.startswith('4')))
        
        revSum = 0
        for revTransaction in revenueTransactions:
            revSum = revSum + float(revTransaction[0])
        budgetItemCalculated['revenue_calculated'] = revSum

        expSum = 0
        for expTransaction in expenditureTransactions:
            expSum = expSum + float(revTransaction[0])
        budgetItemCalculated['expenditure_calculated'] = expSum
        response.append(budgetItemCalculated)
    return response

"""