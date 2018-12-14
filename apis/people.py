from flask_restplus import Namespace, Resource

from .utility import authenticate, schemaToDict

from sql import db

from requests.request import DatabaseRequest
from requests.people_access import UserAccess

from schemas.people import UserSchema, CustomerSchema


api = Namespace('People', description='People related operations.')

dbRequest = DatabaseRequest()

path = 'user'
schema = UserSchema()
model = api.model(path.title(), schemaToDict(schema))
access = UserAccess

@api.route('/'+path)
class User(Resource):
    @api.doc(security='amivapitoken')
    @authenticate()
    def get(self,user):
        accessData = access(user)
        res = dbRequest.getSerializedElements(accessData)
        return res, 200

    @api.doc(security='amivapitoken')
    @api.expect(model)
    @authenticate(requiredUserLevelBit = [9])
    def post(self, user):
        schema.load_commit(api.payload)
        return {'result': path.title() + ' added.'}, 201

@api.route('/'+path+'/<string:id>')
class UserById(Resource):
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
        dbRequest.getElementById(id, accessData).user_privileges = 0
        db.session.commit()
        return {"message": "Operation successful."}, 202