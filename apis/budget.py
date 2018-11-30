from flask_restplus import Namespace, Resource, fields

from sql import db
from sql.budget import BudgetItem, BudgetConfirmed
from sql.transactions import Transaction

from sqlalchemy import or_

from schemas.budget import BudgetConfirmedSchema, BudgetItemSchema


api = Namespace('Budget', description='Budget related operations.')

budgetItemSchema = BudgetItemSchema()
budgetConfirmedSchema = BudgetConfirmedSchema()

@api.route('/')
class Budget(Resource):
    def get(self):
        query = db.session.query(BudgetItem)
        #apply user related filters
        res = [budgetItemSchema.dump(result)[0] for result in query]
        return res


@api.route('/confirmed')
class BudgetConf(Resource):
    def get(self):
        query = db.session.query(BudgetItem, BudgetConfirmed)
        query = query.filter(BudgetItem.financial_year == BudgetConfirmed.financial_year)
        query = query.filter(BudgetItem.budgetitem_id == BudgetConfirmed.budgetitem_id)
        #apply user related filters
        res = []
        for result in query:
            temp = budgetItemSchema.dump(result[0])[0]
            temp.update(budgetConfirmedSchema.dump(result[1])[0])
            res.append(temp)
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

