from main import db

class User(db.Model):
    __tablename__= "USERS"
    # set primary key
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(), unique=True, nullable=False)
    email = db.Column(db.String(), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)
    profile = db.Column(db.String())