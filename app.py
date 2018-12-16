#!flask/bin/python
from flask import Flask
from sql import db
from apis import api
from config import mysqlConfig
from flask_cors import CORS

databaseUri = 'mysql://'+mysqlConfig.user+':'+mysqlConfig.pw+'@'+mysqlConfig.server+'/'+mysqlConfig.database

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = databaseUri
db.init_app(app)
db.app = app
api.init_app(app)

if __name__ == '__main__':
	app.run(debug=True)
	
	
	