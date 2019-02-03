from flask_restplus import Namespace, Resource

from .utility import authenticate, queryDocumentation

from sql import db

from apis.template import EndpointConfiguration
from access.people_access import UserAccess, CustomerAccess



api = Namespace('People', description='People related operations.')

userConfiguration = EndpointConfiguration(api, 'user', UserAccess(), None)

@api.route('/'+userConfiguration.path)
@api.doc(security = 'amivapitoken')
class UserEndpoint(Resource):
    @api.doc(params=queryDocumentation)
    @authenticate()
    def get(self,user):
        return userConfiguration.getRequest(user)
        
    @api.expect(userConfiguration.model)
    @authenticate(requiredUserLevelBit = [9])
    def post(self, user):
        return userConfiguration.postRequest(user)

@api.route('/'+userConfiguration.path+'/<string:id>')
@api.doc(security = 'amivapitoken')
class UserEndpointById(Resource):
    @authenticate()
    def get(self,id,user):
        return userConfiguration.getRequestById(user,id)

    @api.expect(userConfiguration.model)
    @authenticate(requiredUserLevelBit = [9])
    def patch(self,id,user):
        return userConfiguration.patchRequestById(user,id)

    @authenticate(requiredUserLevelBit = [9])
    def delete(self,id,user):
        userConfiguration.getElementById(id, user).user_privileges = 0
        db.session.commit()
        return {"message": "Operation successful."}, 202


customerConfiguration = EndpointConfiguration(api, 'customer', CustomerAccess(), None)

@api.route('/'+customerConfiguration.path)
@api.doc(security = 'amivapitoken')
class CustomerEndpoint(Resource):
    @api.doc(params=queryDocumentation)
    @authenticate(requiredUserLevelBit = [7,9])
    def get(self,user):
        return customerConfiguration.getRequest(user)
        
    # ToDo: Email is not correctly converted to model!
    @api.expect(customerConfiguration.model)
    @authenticate(requiredUserLevelBit = [7,9])
    def post(self, user):
        return customerConfiguration.postRequest(user)

@api.route('/'+customerConfiguration.path+'/<string:id>')
@api.doc(security = 'amivapitoken')
class CustomerEndpointById(Resource):
    @authenticate(requiredUserLevelBit = [7,9])
    def get(self,id,user):
        return customerConfiguration.getRequestById(user,id)

    @api.expect(customerConfiguration.model)
    @authenticate(requiredUserLevelBit = [7,9])
    def patch(self,id,user):
        return customerConfiguration.patchRequestById(user,id)

