from flask import Blueprint, jsonify, request
from main import db
from models.curriculums import Curriculum

curriculums = Blueprint('curriculums', __name__, url_prefix="/curriculums")

@curriculums.route("/", methods=["GET"])
def get_curriculums():
    # get all curriculums from the database
    curriculums_list = Curriculum.query.all()
    # return data from database in JSON format
    result = curriculums_schema.dump(curriculums_list)
    return jsonify(result)

@curriculums.route("/", methods=["POST"])
def create_curriculum():
    # Create a new curriculum
    curriculum_fields = curriculum_schema.load(request.json)
    new_curriculum = Curriculum()
    new_curriculum.user_id = curriculum_fields["user_id"]
    new_curriculum.title = curriculum_fields["title"]
    new_curriculum.description = curriculum_fields["description"]
    # add to database
    db.session.add(new_curriculum)
    db.session.commit()
    return jsonify(curriculum_schema.dump(new_curriculum))

@curriculums.route("/<int:id>/", methods=["DELETE"])
def delete_curriculum():
    # Get ID of user who is attempting to delete
    user_id = get_jwt_identity()
    # Find user in database
    user = User.query.get(user_id)
    # Not a valid user
    if not user:
        return abort(401, description="Invalid user")
    # TODO
        # Make so users can only delete own curriculums
    # Find curriculum to be deleted
    curriculum = Curriculum.query.filter_by(id=id).first()
    # curriculum does not exist
    if not curriculum:
        return abort(400, description="Curriculum does not exist")
    # Delete curriculum from database
    db.session.delete(curriculum)
    db.session.commit()
    return jsonify(curriculum_schema.dump(curriculum))