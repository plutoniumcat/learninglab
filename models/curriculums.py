from main import db

class Curriculum(db.Model):
    __tablename__= "CURRICULUMS"
    # set primary key
    id = db.Column(db.Integer, primary_key=True)
    # set foreign key
    user_id = db.Column(db.Integer, db.ForeignKey("USERS.id"), nullable=False)
    title = db.Column(db.String(), nullable=False)
    description = db.Column(db.String())