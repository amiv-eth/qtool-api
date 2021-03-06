from flask_restplus import Namespace, Resource, fields, abort

from config import amivAPIConfig

from schemas.sessions import AmivapiSessionSchema, AmivapiUserSchema

import requests

from .utility import sessionHandler, authenticate

api = Namespace('Session', description='Session related operations.')

model = api.model('Session', {'amivapi_session_token': fields.String})
sessionSchema = AmivapiSessionSchema()
userSchema = AmivapiUserSchema()

@api.route('/session')
class SessionEndpoint(Resource):
    @api.doc(security = 'amivapitoken')
    @authenticate()
    def get(self,user):
        return sessionHandler.getAllSessions()

    @api.expect(model)
    def post(self):
        token = api.payload['amivapi_session_token']
        sessionRaw = requests.get(
            amivAPIConfig.server+'sessions/'+token,
            headers={
                'Authorization': amivAPIConfig.APItoken,
                'Content-Type': 'application/json'
            },
        )
        if not sessionRaw:
            abort(400, "Session could not be created!")
        session = sessionSchema.load(sessionRaw.json())[0]

        userRaw = requests.get(
            amivAPIConfig.server+'users/'+session['user'],
            headers={
                'Authorization': amivAPIConfig.APItoken,
                'Content-Type': 'application/json'
            },
        )
        if not userRaw:
            abort(400, "User doesn't exist anymore.")
        user = userSchema.load(userRaw.json())[0]
        qtoolSession = sessionHandler.addSession(user)
        return(qtoolSession, 200)