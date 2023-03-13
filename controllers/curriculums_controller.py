from flask import Blueprint, jsonify, request, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from main import db
from models.users import User
from models.curriculums import Curriculum
from models.curriculum_associations import Association
from models.tutorials import Tutorial
from schemas.curriculum_schema import curriculum_schema, curriculums_schema
from schemas.association_schema import association_schema
from schemas.tutorial_schema import tutorial_schema


curriculums = Blueprint('curriculums', __name__, url_prefix="/curriculums")


@curriculums.route("/", methods=["GET"])
def get_curriculums():
    # get all curriculums from the database
    curriculums_list = Curriculum.query.all()
    # return data from database in JSON format
    result = curriculums_schema.dump(curriculums_list)
    return jsonify(result)


# Get curriculum and asssociated tutorials
@curriculums.route("/<int:id>/", methods=["GET"])
def get_curriculum(id):
    # Get curriculum from database
    curriculum = Curriculum.query.filter_by(id=id).first()
    curriculum_info = curriculum_schema.dump(curriculum)
    tutorials = db.session.query(Tutorial).join(Association).join(Curriculum).filter(Curriculum.id==id)
    if tutorials:
        result_list = [curriculum_info]
        for tutorial in tutorials:
            tutorial_dict = tutorial_schema.dump(tutorial)
            tutorial_dict['id'] = tutorial.id
            tutorial_dict['url'] = tutorial.url
            tutorial_dict['user_id'] = tutorial.user_id
            tutorial_dict['title'] = tutorial.title
            tutorial_dict['author'] = tutorial.author
            tutorial_dict['description'] = tutorial.description
            tutorial_dict['level'] = tutorial.level
            tutorial_dict['prerequsites'] = tutorial.prerequisites
            tutorial_dict['pricing'] = tutorial.pricing
            tutorial_dict['length'] = tutorial.length
            result_list.append(tutorial_dict)
        return result_list
    else:
        return abort(404, description="Curriculum not found")


@curriculums.route("/", methods=["POST"])
@jwt_required()
def create_curriculum():
    # Get ID of user who is attempting to add
    user_id = get_jwt_identity()
    # Find user in database
    user = User.query.get(user_id)
    # Not a valid user
    if not user:
        return abort(401, description="Invalid user")
    # Create a new curriculum
    curriculum_fields = curriculum_schema.load(request.json)
    new_curriculum = Curriculum()
    new_curriculum.user_id = user_id
    new_curriculum.title = curriculum_fields["title"]
    new_curriculum.description = curriculum_fields["description"]
    # add to database
    db.session.add(new_curriculum)
    db.session.commit()
    return jsonify(curriculum_schema.dump(new_curriculum))


@curriculums.route("/<int:id>/", methods=["DELETE"])
@jwt_required()
def delete_curriculum(id):
    # Get ID of user who is attempting to delete
    user_id = get_jwt_identity()
    # Find user in database
    user = User.query.get(user_id)
    # Not a valid user
    if not user:
        return abort(401, description="Invalid user")
    # Find curriculum to be deleted
    curriculum = Curriculum.query.filter_by(id=id).first()
    # Check curriculum exists and belongs to user
    if not curriculum:
        return abort(400, description="Curriculum does not exist")
    elif curriculum.user_id != int(user_id):
        return abort(403, description="Not authorized to alter this curriculum.")
    # Delete curriculum from database
    db.session.delete(curriculum)
    db.session.commit()
    return jsonify(curriculum_schema.dump(curriculum))


@curriculums.route("/<int:id>/", methods=["POST"])
@jwt_required()
def add_to_curriculum(id):
    # Get ID of user who is attempting to add
    user_id = get_jwt_identity()
    # Find user in database
    user = User.query.get(user_id)
    # Not a valid user
    if not user:
        return abort(401, description="Invalid user")
    # Find curriculum to be edited
    curriculum = Curriculum.query.filter_by(id=id).first()
    # curriculum does not exist
    if not curriculum:
        return abort(400, description="Curriculum does not exist")
    elif curriculum.user_id != int(user_id):
        return abort(403, description="Not authorized to alter this curriculum.")
    # Create new association
    association_fields = association_schema.load(request.json)
    new_association = Association()
    new_association.curriculum_id = id
    new_association.tutorial_id = association_fields["tutorial_id"]
    db.session.add(new_association)
    db.session.commit()
    return jsonify(association_schema.dump(new_association))