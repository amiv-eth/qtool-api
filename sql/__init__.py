from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()

class BaseModel(db.Model):
    __abstract__ = True
    _created = db.Column(db.DATE, default = datetime.datetime.now, nullable= False)
    _updated = db.Column(db.DATE, onupdate = datetime.datetime.now, nullable= False)