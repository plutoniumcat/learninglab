from sqlalchemy.orm import relationship
from main import db

class Tutorial(db.Model):
    __tablename__= "TUTORIALS"
    # set primary key
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(), unique=True, nullable=False)
    # set foreign key
    user_id = db.Column(db.Integer, db.ForeignKey("USERS.id"), nullable=False)
    title = db.Column(db.String(), nullable=False)
    author = db.Column(db.String(), nullable=False)
    description = db.Column(db.String())
    level = db.Column(db.String())
    prerequisites = db.Column(db.String())
    pricing = db.Column(db.Integer)
    length = db.Column(db.String())
    association = relationship("Association", cascade="all, delete-orphan")