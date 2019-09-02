from sql import db,BaseModel


class TransactionType(BaseModel):
    type_id = db.Column(db.Integer, nullable= False, primary_key=True)
    type_class = db.Column(db.String(31), nullable= False)
    type_name = db.Column(db.String(31), nullable= False)


class TransactionAccount(BaseModel):
    account_id = db.Column(db.Integer, nullable = False, primary_key=True)
    account_name = db.Column(db.String(255), nullable = False)


class TransactionCategory(BaseModel):
    category_id = db.Column(db.Integer, nullable = False, primary_key=True)
    category_name = db.Column(db.String(255), nullable = False)


class TransactionCurrency(BaseModel):
    currency_id = db.Column(db.Integer, nullable = False, primary_key=True)
    currency_name = db.Column(db.String(255), nullable = False)
    currency_shortcut = db.Column(db.String(3), nullable = False)
