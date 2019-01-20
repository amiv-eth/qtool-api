from requests import AccessControl

# Databases
from sql.people import User, Customer

# Schemas
from schemas.people import UserSchema, CustomerSchema

class UserAccess(AccessControl):
    def specifyDatabase(self):
        self.databaseName = User
        self.databasePrimaryKey = User.user_id
        self.schemaBase = UserSchema
    def getUserLevelFilters(self, user):
        return True

    def getUserLevelSchema(self, user):
        return UserSchema(exclude = ('password', 'salt',))

class CustomerAccess(AccessControl):
    def specifyDatabase(self):
        self.databaseName = Customer
        self.databasePrimaryKey = Customer.customer_id
        self.schemaBase = CustomerSchema
        
    def getUserLevelFilters(self, user):
        return True

    def getUserLevelSchema(self,user):
        return CustomerSchema()