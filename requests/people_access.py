from schemas.people import UserSchema, CustomerSchema
from sql.people import User, Customer

from .access_control import AccessControl

class UserAccess(AccessControl):
    def specifyDatabase(self):
        self.databaseName = User
        self.primaryKey = User.user_id

    def applyUserLevelFilters(self, user):
        return True

    def selectUserLevelSchema(self, user):
        return UserSchema(exclude = ('password', 'salt',))