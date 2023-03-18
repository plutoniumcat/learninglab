from flask import Blueprint, jsonify, request, abort
from sqlalchemy import update
from functools import wraps
from main import db
from models.curriculums import Curriculum
from models.curriculum_associations import Association
from models.tutorials import Tutorial
from schemas.curriculum_schema import curriculum_schema, curriculums_schema
from schemas.association_schema import association_schema
from schemas.tutorial_schema import tutorial_schema
from controllers.auth_controller import authenticate_user, error_handler

curriculums = Blueprint('curriculums', __name__, url_prefix="/curriculums")


def curriculum_auth(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        user_id = kwargs["user_id"]
        id = kwargs.get("id")
        # Find curriculum to be deleted
        curriculum = Curriculum.query.filter_by(id=id).first()
        kwargs["curriculum"] = curriculum
        # Check curriculum exists and belongs to user
        if not curriculum:
            return abort(400, description="Curriculum does not exist")
        elif curriculum.user_id != int(user_id):
            return abort(403, description="Not authorized to alter this curriculum.")
        return f(*args, **kwargs)
    return decorator


@curriculums.route("/", methods=["GET"])
@error_handler
def get_curriculums():
    # get all curriculums from the database
    curriculums_list = Curriculum.query.all()
    # return data from database in JSON format
    result = curriculums_schema.dump(curriculums_list)
    return jsonify(result)


# Get curriculum and asssociated tutorials
@curriculums.route("/<int:id>/", methods=["GET"])
@error_handler
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
@authenticate_user
@error_handler
def create_curriculum(**kwargs):
    user_id = kwargs["user_id"]
    # Create a new curriculum
    curriculum_fields = curriculum_schema.load(request.json)
    new_curriculum = Curriculum()
    new_curriculum.user_id = user_id
    new_curriculum.title = curriculum_fields["title"]
    if curriculum_fields.get("description") is not None:
        new_curriculum.description = curriculum_fields["description"]
    # add to database
    db.session.add(new_curriculum)
    db.session.commit()
    return jsonify(curriculum_schema.dump(new_curriculum))


@curriculums.route("/<int:id>/", methods=["DELETE"])
@authenticate_user
@curriculum_auth
@error_handler
def delete_curriculum(**kwargs):
    curriculum = kwargs["curriculum"]
    # Delete curriculum from database
    db.session.delete(curriculum)
    db.session.commit()
    return jsonify(curriculum_schema.dump(curriculum))


@curriculums.route("/<int:id>/edit", methods=["POST"])
@authenticate_user
@curriculum_auth
@error_handler
def edit_curriculum(id, **kwargs):
    user_id = kwargs["user_id"]
    # Find curriculum to be edited
    curriculum = Curriculum.query.filter_by(id=id).first()
    # curriculum does not exist
    if not curriculum:
        return abort(400, description="Curriculum does not exist")
    elif curriculum.user_id != int(user_id):
        return abort(403, description="Not authorized to alter this curriculum")
    curriculum_fields = request.json
    update_dict = {}
    for field in curriculum_fields:
        if curriculum_fields[field] is not None:
            update_dict[field] = curriculum_fields[field]
    update_curriculum = update(Curriculum).where(Curriculum.id==id).values(update_dict)
    # add to database
    db.session.execute(update_curriculum)
    db.session.commit()
    return jsonify(curriculum_schema.dump(curriculum))


@curriculums.route("/<int:id>/add", methods=["POST"])
@authenticate_user
@curriculum_auth
@error_handler
def add_to_curriculum(id, **kwargs):
    user_id = kwargs["user_id"]
    # Find curriculum to be edited
    curriculum = Curriculum.query.filter_by(id=id).first()
    # curriculum does not exist
    if not curriculum:
        return abort(400, description="Curriculum does not exist")
    elif curriculum.user_id != int(user_id):
        return abort(403, description="Not authorized to alter this curriculum")
    # Create new association
    association_fields = association_schema.load(request.json)
    new_association = Association()
    new_association.curriculum_id = id
    new_association.tutorial_id = association_fields["tutorial_id"]
    db.session.add(new_association)
    db.session.commit()
    return jsonify(association_schema.dump(new_association))


#Remove tutorial from curriculum
@curriculums.route("/<int:id>/<int:tutorial_id>/", methods=["DELETE"])
@authenticate_user
@curriculum_auth
@error_handler
def delete_from_curriculum(id, tutorial_id, **kwargs):
    # Find association between curriculum and tutorial
    association = Association.query.filter_by(curriculum_id=id, tutorial_id=tutorial_id).first()
    db.session.delete(association)
    db.session.commit()
    return {"message": "Tutorial successfully removed from curriculum"}
