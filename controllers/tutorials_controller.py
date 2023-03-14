from flask import Blueprint, jsonify, request, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import update
from main import db
from models.tutorials import Tutorial
from models.users import User
from schemas.tutorial_schema import tutorial_schema, tutorials_schema

tutorials = Blueprint('tutorials', __name__, url_prefix="/tutorials")

# Get all tutorials
@tutorials.route("/", methods=["GET"])
def get_tutorials():
    # get all tutorials from the database
    tutorials_list = Tutorial.query.all()
    # return data from database in JSON format
    result = tutorials_schema.dump(tutorials_list)
    return jsonify(result)


# Get tutorial by id
@tutorials.route("/<int:id>/", methods=["GET"])
def get_tutorial(id):
    # get tutorial with id from database
    tutorial = Tutorial.query.filter_by(id=id).first()
    result = tutorial_schema.dump(tutorial)
    return jsonify(result)


# Get all tutorials added by a user
@tutorials.route("/users/<int:user_id>", methods=["GET"])
def get_tutorial_by_user(user_id):
    # Get all tutorials with user id
    tutorials_list = Tutorial.query.filter_by(user_id=user_id)
    result = tutorials_schema.dump(tutorials_list)
    return jsonify(result)


# Get all tutorials by an author
@tutorials.route("authors/<string:author>", methods=["GET"])
def get_tutorial_by_author(author):
    tutorials_list = Tutorial.query.filter_by(author=author)
    result = tutorials_schema.dump(tutorials_list)
    return jsonify(result)


@tutorials.route("/", methods=["POST"])
@jwt_required()
def create_tutorial():
    # Get ID of user who is attempting to add
    user_id = get_jwt_identity()
    # Find user in database
    user = User.query.get(user_id)
    # Not a valid user
    if not user:
        return abort(401, description="Invalid user")
    # Create a new tutorial
    tutorial_fields = tutorial_schema.load(request.json)
    new_tutorial = Tutorial()
    new_tutorial.url = tutorial_fields["url"]
    new_tutorial.user_id = user_id
    new_tutorial.title = tutorial_fields["title"]
    new_tutorial.author = tutorial_fields["author"]
    if tutorial_fields.get("description") is not None:
        new_tutorial.description = tutorial_fields["description"]
    if tutorial_fields.get("level") is not None:
        new_tutorial.level = tutorial_fields["level"]
    if tutorial_fields.get("prerequisites") is not None:
        new_tutorial.prerequisites = tutorial_fields["prerequisites"]
    if tutorial_fields.get("pricing") is not None:
        new_tutorial.pricing = tutorial_fields["pricing"]
    if tutorial_fields.get("length") is not None:
        new_tutorial.length = tutorial_fields["length"]
    # add to database
    db.session.add(new_tutorial)
    db.session.commit()
    return jsonify(tutorial_schema.dump(new_tutorial))


# Edit tutorial
@tutorials.route("/<int:id>/edit", methods=["POST"])
@jwt_required()
def edit_tutorial(id):
    # Get ID of user who is attempting to edit
    user_id = get_jwt_identity()
    # Find user in database
    user = User.query.get(user_id)
    # Not a valid user
    if not user:
        return abort(401, description="Invalid user")
    # Find tutorial to be edited
    tutorial = Tutorial.query.filter_by(id=id).first()
    # Tutorial does not exist
    if not tutorial:
        return abort(400, description="Tutorial does not exist")
    elif int(user_id) != tutorial.user_id:
        return abort(401, description="Not authorized to edit this tutorial")
    tutorial_fields = request.json
    update_dict = {}
    for field in tutorial_fields:
        if tutorial_fields[field] is not None:
            update_dict[field] = tutorial_fields[field]
    update_tutorial = update(Tutorial).where(Tutorial.id==id).values(update_dict)
    # add to database
    db.session.execute(update_tutorial)
    db.session.commit()
    return jsonify(tutorial_schema.dump(tutorial))


@tutorials.route("/<int:id>/", methods=["DELETE"])
@jwt_required()
def delete_tutorial(id):
    # Get ID of user who is attempting to delete
    user_id = get_jwt_identity()
    # Find user in database
    user = User.query.get(user_id)
    # Not a valid user
    if not user:
        return abort(401, description="Invalid user")
    elif not user.admin:
        return abort(401, description="Not authorized to delete tutorials")
    # Find tutorial to be deleted
    tutorial = Tutorial.query.filter_by(id=id).first()
    # Tutorial does not exist
    if not tutorial:
        return abort(400, description="Tutorial does not exist")
    # Delete tutorial from database
    db.session.delete(tutorial)
    db.session.commit()
    return jsonify(tutorial_schema.dump(tutorial))