from main import db

class Association(db.Model):
    __tablename__= "CURRICULUM_ASSOCIATIONS"
    # set foreign keys as composite primary key
    curriculum_id = db.Column(db.Integer, db.ForeignKey("CURRICULUMS.id"), primary_key=True, nullable=False)
    tutorial_id = db.Column(db.Integer, db.ForeignKey("TUTORIALS.id"), primary_key=True, nullable=False)