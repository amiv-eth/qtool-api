class AccessControl():
    databaseName = None
    primaryKey = None
    schema = None
    userLevelFilters = True

    def __init__(self, user):
        self.specifyDatabase()
        self.schema = self.selectUserLevelSchema(user)
        self.userLevelFilters = self.applyUserLevelFilters(user)

    def specifyDatabse(self):
        print ("You are using the method specifyDatabse of the abstract class AccessControl, please redefine this method when inherting it!")
        raise TypeError

    def applyUserLevelFilters(self, user):
        print ("You are using the method applyUserLevelFilters of the abstract class AccessControl, please redefine this method when inherting it!")
        raise TypeError
        return True

    def selectUserLevelSchema(self, user):
        print ("You are using the method selectUserLevelSchema of the abstract class AccessControl, please redefine this method when inherting it!")
        raise TypeError
        return None


