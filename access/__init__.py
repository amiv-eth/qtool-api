from marshmallow import Schema, post_load

class AccessControl():
    databaseName = None
    databasePrimaryKey = None
    schemaBase = None

    def __init__(self, user):
        self.specifyDatabase()

    def specifyDatabse(self):
        print ("You are using the method specifyDatabse of the abstract class AccessControl, please redefine this method when inherting it!")
        raise TypeError

    def getUserLevelFilters(self, user):
        print ("You are using the method getUserLevelFilters of the abstract class AccessControl, please redefine this method when inherting it!")
        raise TypeError
        return True

    def getUserLevelSchema(self, user):
        print ("You are using the method getUserLevelSchema of the abstract class AccessControl, please redefine this method when inherting it!")
        raise TypeError
        return None
        

class EmbeddingSchema(Schema):
    accessData = {}
    
    @post_load
    def mask_data(self, data):
        maskedAccessData = {}
        for key in data:
            if data[key]:
                maskedAccessData[key] = self.accessData[key]
        return maskedAccessData