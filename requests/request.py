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

    def embedElement(self, accessControl, embeddedData, embedingFilters = True):
        userLevelFilters = accessControl.userLevelFilters
        query = db.session.query(accessControl.databaseName)
        for element in embeddedData:
            userLevelFilters = and_(userLevelFilters, embeddedData[element].userLevelFilters)
            query = query.add_entity(embeddedData[element].databaseName)
            query = query.join(embeddedData[element].databaseName)
        response = []
        for result in query:
            primaryItem = accessControl.schema.dump(result[0])[0]
            for idx, element in enumerate(embeddedData):
                primaryItem[element] = embeddedData[element].schema.dump(result[idx+1])[0]
            response.append(primaryItem)
        return response


    def getSerializedElements(self, accessControl):
        query = db.session.query(accessControl.databaseName).filter(accessControl.userLevelFilters)
        response = [accessControl.schema.dump(result)[0] for result in query]
        return response

    """
    def getSerializedElements(self, schema, userLevelFilters = True, queryFilters = True):
        query = db.session.query(self.databaseName).filter(and_(userLevelFilters,queryFilters))
        # ToDo check for errors
        response = [schema.dump(result)[0] for result in query]
        return response
    """

    def getSerializedElementById(self, id, accessControl):
        element = self.getObjectById(id,accessControl)
        return accessControl.schema.dump(element)[0]

    def getObjectById(self, id, accessControl):
        query = db.session.query(accessControl.databaseName).filter(accessControl.primaryKey == id)
        if not query.first():
            abort(404, 'Id does not exist.')
        query = query.filter(accessControl.userLevelFilters)
        if not query.first():
            abort(401, 'User not authorized.')
        return query.first()
            

