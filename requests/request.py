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
    def getSerializedResponse(self, user, DatabaseAccessClass, page = 1, sort = None, embedded = {}, perPage = 25, where = True):
        primaryDatabaseAccess = DatabaseAccessClass(user)
        secondaryDatabaseAccess = {}
        for key in embedded:
            secondaryDatabaseAccess[key] = embedded[key](user)

        # Initialize filters and query
        userLevelFilters = primaryDatabaseAccess.userLevelFilters
        query = db.session.query(primaryDatabaseAccess.databaseName)

        # Join with all tables that are embedded
        # ToDo: Embedding should yield left join in Transaction instead of innerjoin
        for key in secondaryDatabaseAccess:
            accessData = secondaryDatabaseAccess[key]
            userLevelFilters = and_(userLevelFilters, accessData.userLevelFilters)
            query = query.add_entity(accessData.databaseName).outerjoin(accessData.databaseName)

        # Apply user level filters
        query = query.filter(userLevelFilters)
        # Apply query http query filters
        query = query.filter(where)

        # Apply query input and generate meta data
        totalResults = query.count()
        query = query.order_by(sort)
        query = query.limit(perPage).offset(perPage*(page-1))
        resultsOnPage = query.count()

        # Construct response
        # ToDo: Catch possible errors when dumping
        items = []
        for result in query:
            if embedded:
                primaryItem = primaryDatabaseAccess.schema.dump(result[0])[0]
            else:
                primaryItem = primaryDatabaseAccess.schema.dump(result)[0]
            for idx, key in enumerate(secondaryDatabaseAccess):
                primaryItem[key] = secondaryDatabaseAccess[key].schema.dump(result[idx+1])[0]
            items.append(primaryItem)
        response = {'items': items}
        response['meta'] = {'page': page, 'results_on_this_page': resultsOnPage, 'max_results_per_page': perPage, 'total_results': totalResults}
        return response


    def getSerializedElementById(self, id, accessControl):
        element = self.getElementById(id,accessControl)
        return accessControl.schema.dump(element)[0]

    def patchElement(self, id , accessControl, newData):
        element = self.getElementById(id, accessControl)
        for key in newData:
            setattr(element, key, newData[key])
        db.session.commit()
        return {'message': 'Operation successful.'}, 202

    def getElementById(self, id, accessControl):
        query = db.session.query(accessControl.databaseName).filter(accessControl.primaryKey == id)
        if not query.first():
            abort(404, 'Id does not exist.')
        query = query.filter(accessControl.userLevelFilters)
        if not query.first():
            abort(401, 'User not authorized.')
        return query.first()
            

