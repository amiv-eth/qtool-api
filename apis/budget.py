from flask_restplus import Namespace, Resource

from sql.budget import BudgetItem

from sql import db
from sql.transactions import Transaction

from .utility import authenticate

from sqlalchemy import or_

from schemas.budget import BudgetConfirmedSchema, BudgetItemSchema

from requests.budget_access import BudgetConfirmedAccess, BudgetItemAccess
from requests.request import DatabaseRequest


api = Namespace('Budget', description='Budget related operations.')

budgetItemSchema = BudgetItemSchema()
budgetConfirmedSchema = BudgetConfirmedSchema()

dbRequest = DatabaseRequest()

@api.route('/')
class Budget(Resource):
    @api.doc(security='amivapitoken')
    @authenticate()
    def get(self, user):
        budgetAccessData = BudgetItemAccess(user)
        return dbRequest.getSerializedElements(budgetAccessData)


@api.route('/confirmed')
class BudgetConf(Resource):
    @api.doc(security='amivapitoken')
    @authenticate()
    def get(self,user):
        budgetAccessData = BudgetItemAccess(user)
        budgetConfAccessData = BudgetConfirmedAccess(user)
        res = dbRequest.embedElement(budgetConfAccessData,{'budget_item':budgetAccessData})
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

