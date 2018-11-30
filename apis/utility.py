from flask import request
from functools import wraps

from sql import db
from sql.people import User


def authenticate(f):
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
		elif token == 'blitz-quaestor':
			user = query.filter(User.user_id == 7).first()
		elif token == "quaestor":
			user = query.filter(User.user_id == 100).first()
		else:
			return {"message": "User not logged in."}, 401
		return f(user = user,*args,**kwargs)
	return decorated