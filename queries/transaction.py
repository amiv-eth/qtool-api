from schemas.transaction import TransactionSchema
from sql.transactions import Transaction


class TransactionQueries():
    databaseName = Transaction
    idField = TransactionSchema

    userLevelSchema = {}
    queryParameters = {}

    def getElements():
        return 