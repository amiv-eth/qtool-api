from .utility import schemaToDict

from apis.query_parser import queryParser

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

            


class EndpointConfiguration():
    def __init__(self, api, path, access, embeddable):
        self.api = api
        self.path = path
        self.databaseName = access.databaseName
        self.access = access
        self.baseSchema = access.schemaBase()
        self.embeddable = embeddable
        self.model = api.model(path.title(), schemaToDict(access.schemaBase))


    def getRequest(self, user):
        args = queryParser(self.databaseName, self.embeddable)
        res = self.getSerializedResponse(user, **args)
        return res, 200

    def postRequest(self,user):
        self.baseSchema.load_commit(self.api.payload)
        return {'result': self.path.title() + ' added.'}, 201

    def getRequestById(self,user,id):
        return self.getSerializedElementById(user,id)

    def patchRequestById(self,user,id):
        newData = self.baseSchema.load(self.api.payload)[0]
        return self.patchElement(id,user,newData)

    def getSerializedResponse(self, user, page = 1, sort = None, embedded = {}, perPage = 25, where = True):
        primaryDatabaseAccess = self.access
        secondaryDatabaseAccess = {}
        for key in embedded:
            secondaryDatabaseAccess[key] = embedded[key]()

        # Initialize filters and query
        userLevelFilters = primaryDatabaseAccess.getUserLevelFilters(user)
        query = db.session.query(primaryDatabaseAccess.databaseName)

        # Join with all tables that are embedded
        # ToDo: Embedding should yield left join in Transaction instead of innerjoin
        for key in secondaryDatabaseAccess:
            accessData = secondaryDatabaseAccess[key]
            userLevelFilters = and_(userLevelFilters, accessData.getUserLevelFilters(user))
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
                primaryItem = primaryDatabaseAccess.getUserLevelSchema(user).dump(result[0])[0]
            else:
                primaryItem = primaryDatabaseAccess.getUserLevelSchema(user).dump(result)[0]
            for idx, key in enumerate(secondaryDatabaseAccess):
                primaryItem[key] = secondaryDatabaseAccess[key].getUserLevelSchema(user).dump(result[idx+1])[0]
            items.append(primaryItem)
        response = {'items': items}
        response['meta'] = {'page': page, 'results_on_this_page': resultsOnPage, 'max_results_per_page': perPage, 'total_results': totalResults}
        return response


    def getSerializedElementById(self, user, id):
        element = self.getElementById(id,user)
        return self.access.getUserLevelSchema(user).dump(element)[0]

    def patchElement(self, id , user, newData):
        element = self.getElementById(id, user)
        for key in newData:
            setattr(element, key, newData[key])
        db.session.commit()
        return {'message': 'Operation successful.'}, 202

    def getElementById(self, id, user):
        query = db.session.query(self.access.databaseName).filter(self.access.databasePrimaryKey == id)
        if not query.first():
            abort(404, 'Id does not exist.')
        query = query.filter(self.access.getUserLevelFilters(user))
        if not query.first():
            abort(401, 'User not authorized.')
        return query.first()
