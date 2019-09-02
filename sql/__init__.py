from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()

class BaseModel(db.Model):
    __abstract__ = True
    _created = db.Column(db.DATETIME, default = datetime.datetime.now, nullable= False)
    _updated = db.Column(db.DATETIME, default = datetime.datetime.now, onupdate = datetime.datetime.now, nullable= False)