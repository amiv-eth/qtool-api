from flask import request
from functools import wraps

from sql import db
from sql.people import User


def authenticate(requireUserLevelBit = None):
	def decorator(f):
		@wraps(f)
		def decorated(*args, **kwargs):
			if 'X-AMIV-API-TOKEN' in request.headers:
				token = request.headers['X-AMIV-API-TOKEN']
			else:
				return {"message": "User not logged in."}, 401
			query = db.session.query(User)
			#ToDo: Fetch real users by token number
			if token == 'iv-user':
				user = query.filter(User.user_id == 108).first()
			elif token == 'merch-admin':
				user = query.filter(User.user_id == 2).first()
			elif token == 'brauko-quaestor':
				user = query.filter(User.user_id == 7).first()
			elif token == 'blitz-quaestor':
				user = query.filter(User.user_id == 999).first()
			elif token == "quaestor":
				user = query.filter(User.user_id == 100).first()
			else:
				return {"message": "User not logged in."}, 401
			
			if requireUserLevelBit:
				if not (user.user_privileges>>requireUserLevelBit)&1:
					return {"message": "User not authorized."}, 401
			return f(user = user,*args,**kwargs)
		return decorated
	return decorator

def checkForExistence(table, column, key = 'id'):
	def decorator(f):
	    @wraps(f)
	    def decorated(*args, **kwargs):
	        element = db.session.query(table).filter(column == kwargs[key]).first()
	        if not element:
	            return {'message': 'Id does not exist!'}, 404
	        return f(element = element,*args,**kwargs)
	    return decorated
	return decorator
