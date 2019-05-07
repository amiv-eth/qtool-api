from flask_restplus import Namespace, Resource

from sql import db

from sqlalchemy import or_

from .utility import authenticate, queryDocumentation

from access.budget_access import BudgetItemAccess, BudgetGroupAccess, BudgetItemEmbeddable
from access.transaction_access import TransactionAccess
from apis.template import EndpointConfiguration


api = Namespace('Budget', description='Budget related operations.')

budgetItemConfiguration = EndpointConfiguration(api, 'item', BudgetItemAccess(), BudgetItemEmbeddable())


@api.route('/'+budgetItemConfiguration.path)
@api.doc(security = 'amivapitoken')
class BudgetItemEndpoint(Resource):
    @api.doc(params=queryDocumentation)
    @authenticate()
    def get(self,user):
        [response, code] = budgetItemConfiguration.getRequest(user)
        calculateBudget(response['items'])
        return response, code
        
    @api.expect(budgetItemConfiguration.model)
    @authenticate(requiredUserLevelBit = [9])
    def post(self, user):
        return budgetItemConfiguration.postRequest(user)

@api.route('/'+budgetItemConfiguration.path+'/<string:id>')
@api.doc(security = 'amivapitoken')
class BudgetItemEndpointById(Resource):
    @authenticate()
    def get(self,id,user):
        response = budgetItemConfiguration.getRequestById(user,id)
        calculateBudget([response])
        return response

    @api.expect(budgetItemConfiguration.model)
    @authenticate(requiredUserLevelBit = [9])
    def patch(self,id,user):
        return budgetItemConfiguration.patchRequestById(user,id)

    @authenticate(requiredUserLevelBit = [9])
    def delete(self,id,user):
        budgetItemConfiguration.getElementById(id, user).budgetitem_code = "0"
        db.session.commit()
        return {"message": "Operation successful."}, 202


budgetGroupConfiguration = EndpointConfiguration(api, 'group', BudgetGroupAccess(), None)

@api.route('/'+budgetGroupConfiguration.path)
@api.doc(security = 'amivapitoken')
class BudgetGroupEndpoint(Resource):
    @api.doc(params=queryDocumentation)
    @authenticate()
    def get(self,user):
        return budgetGroupConfiguration.getRequest(user)
        
    @api.expect(budgetGroupConfiguration.model)
    @authenticate(requiredUserLevelBit = [9])
    def post(self, user):
        return budgetGroupConfiguration.postRequest(user)

@api.route('/'+budgetGroupConfiguration.path+'/<string:id>')
@api.doc(security = 'amivapitoken')
class BudgetGroupEndpointById(Resource):
    @authenticate()
    def get(self,id,user):
        return budgetGroupConfiguration.getRequestById(user,id)

    @api.expect(budgetGroupConfiguration.model)
    @authenticate(requiredUserLevelBit = [9])
    def patch(self,id,user):
        return budgetGroupConfiguration.patchRequestById(user,id)


# ToDo: Add means to query by calculated results!
# ToDo: Cache results!

def calculateBudget(serializedResponseList):
    Transaction = TransactionAccess().databaseName
    for serializedBudgetItem in serializedResponseList:
        budgetitem_id = serializedBudgetItem['budgetitem_id']
        
        transactions = db.session.query(Transaction.amount_in_chf).filter(Transaction.budgetitem_id == budgetitem_id)
        revenueTransactions = transactions.filter(or_(Transaction.type_id.startswith('1'),Transaction.type_id.startswith('3')))
        expenditureTransactions = transactions.filter(or_(Transaction.type_id.startswith('2'),Transaction.type_id.startswith('4')))
        
        revSum = 0
        for revTransaction in revenueTransactions:
            if revTransaction[0]:
                revSum = revSum + float(revTransaction[0])
        serializedBudgetItem['revenue_calculated'] = revSum

        expSum = 0
        for expTransaction in expenditureTransactions:
            if expTransaction[0]:
                expSum = expSum + float(expTransaction[0])
        serializedBudgetItem['expenditure_calculated'] = expSum

