from sqlalchemy import and_

from flask_restplus import abort

from sql import db
import enum

class UserLevels(enum.Enum):
    user = 0
    iv_user = 1
    merch_user = 2
    merch_admin = 3
    bastli_user = 4
    bastli_admin = 5
    kommissionspq = 6
    invoice_user = 7
    revisor = 8
    quaestor = 9


class DatabaseRequest():
    databaseName = None
    primaryKey = None

    def getSerializedElements(self, schema, userLevelFilters = True, queryFilters = True):
        query = db.session.query(self.databaseName).filter(and_(userLevelFilters,queryFilters))
        # ToDo check for errors
        response = [schema.dump(result)[0] for result in query]
        return response

    def getSerializedElementById(self, id, schema, userLevelFilters = True):
        element = self.getObjectById(id,userLevelFilters)
        return schema.dump(element)[0]

    def getObjectById(self, id, userLevelFilters = True):
        query = db.session.query(self.databaseName).filter(self.primaryKey == id)
        if not query.first():
            abort(404, 'Id does not exist.')
        query = query.filter(userLevelFilters)
        if not query.first():
            abort(401, 'User not authorized.')
        return query.first()
            

