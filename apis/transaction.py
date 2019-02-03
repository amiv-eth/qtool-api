from flask_restplus import Namespace, Resource

from .utility import authenticate, queryDocumentation

from sql import db

from apis.template import EndpointConfiguration

from access.transaction_access import TransactionAccess, ReceiptAccess, TransactionEmbeddable, ReceiptEmbeddable


api = Namespace('Transaction', description='Transaction related operations.')

transactionConfiguration = EndpointConfiguration(api, 'transaction', TransactionAccess(), TransactionEmbeddable())

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

receiptConfiguration = EndpointConfiguration(api, 'receipt', ReceiptAccess(), ReceiptEmbeddable())

@api.route('/'+receiptConfiguration.path)
class ReceiptEndpoint(Resource):
    @api.doc(params=queryDocumentation, security = 'amivapitoken')
    @authenticate()
    def get(self,user):
        return receiptConfiguration.getRequest(user)
