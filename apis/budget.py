from flask_restplus import Namespace, Resource

from sql import db

from .utility import authenticate, queryDocumentation


from access.budget_access import BudgetConfirmedAccess, BudgetItemAccess
from apis.template import EndpointConfiguration


api = Namespace('Budget', description='Budget related operations.')

budgetItemConfiguration = EndpointConfiguration(api, 'item', BudgetItemAccess(), None)


@api.route('/'+budgetItemConfiguration.path)
@api.doc(security = 'amivapitoken')
class BudgetItemEndpoint(Resource):
    @api.doc(params=queryDocumentation)
    @authenticate()
    def get(self,user):
        return budgetItemConfiguration.getRequest(user)
        
    @api.expect(budgetItemConfiguration.model)
    @authenticate(requiredUserLevelBit = [9])
    def post(self, user):
        return budgetItemConfiguration.postRequest(user)

@api.route('/'+budgetItemConfiguration.path+'/<string:id>')
@api.doc(security = 'amivapitoken')
class BudgetItemEndpointById(Resource):
    @authenticate()
    def get(self,id,user):
        return budgetItemConfiguration.getRequestById(user,id)

    @api.expect(budgetItemConfiguration.model)
    @authenticate(requiredUserLevelBit = [9])
    def patch(self,id,user):
        return budgetItemConfiguration.patchRequestById(user,id)

    @authenticate(requiredUserLevelBit = [9])
    def delete(self,id,user):
        budgetItemConfiguration.getElementById(id, user).financial_year = -1
        db.session.commit()
        return {"message": "Operation successful."}, 202

budgetItemConfConfiguration = EndpointConfiguration(api, 'confirmed', BudgetConfirmedAccess(), None)

@api.route('/'+budgetItemConfConfiguration.path)
@api.doc(security='amivapitoken')
class BudgetConfEndpoint(Resource):
    @api.doc(params=queryDocumentation)
    @authenticate()
    def get(self,user):
        return budgetItemConfConfiguration.getRequest(user)
# Post and patch: link creation of entries to budgetitem


# Add means to cache and query results
"""
@api.route('/calculated')
class BudgetCalculated(Resource):
    def get(self):
        #ToDo: Cache result
        values = calculateBudget()
        return values

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