from sql import db, BaseModel


association_table = db.Table('association_user_budgetitem', BaseModel.metadata,
    db.Column('user_id', db.Integer, db.ForeignKey('user.user_id')),
    db.Column('budgetitem_id', db.Integer, db.ForeignKey('budget_item.budgetitem_id'))
)


class Customer(BaseModel):
    customer_id = db.Column(db.Integer, nullable = False, primary_key=True)
    category = db.Column(db.String(255), nullable=False)
    company = db.Column(db.String(255), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    plz = db.Column(db.String(255), nullable=False)
    city = db.Column(db.String(255), nullable=False)
    country = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    quotation = db.Column(db.String(255), nullable=False)


class User(BaseModel):
    user_id = db.Column(db.Integer, nullable = False, primary_key=True)
    nethz = db.Column(db.String(255), nullable = False)
    password = db.Column(db.String(255), nullable = False)
    salt = db.Column(db.String(255), nullable = False)
    name = db.Column(db.String(255), nullable = False)
    iban = db.Column(db.String(255), nullable = False)
    bic = db.Column(db.String(255), nullable = False)
    role = db.Column(db.String(255), nullable=False)
    amiv_email = db.Column(db.String(255), nullable=False)
    user_privileges = db.Column(db.Integer, nullable=False)
    own_budgetitem_id = db.relationship("BudgetItem",secondary=association_table)



"""
User privileges
   0 - 0 User blocked: can only read budget previews
   1 - 0 User: can add Belegformular and review own belege
   2 - 1 IV-User: can add iv and reveiw own iv
   4 - 2 Merch-User: can sell articles with merch kasse and review transactions
   8 - 3 Merch-Admin: can edit merch articles (implicitly gets 4)
  16 - 4 Bastlikassen-User: can sell articles from bastli kasse and review transactions
  32 - 5 Bastlikassen-admin: can edit articles (implicitly gets 16), only needed if bastli articles are integrated in database
  64 - 6 KommissionsPQ/Ressort: can review transactions of a predefined budgetitems (implicitely gets 2) -> saved as coma separated list
 128 - 7 Rechnung-User: can create and edit invoices
 256 - 8 Revisor/Praesi: can review all transactions
 512 - 9 Quaestor: can edit an review everything
"""
