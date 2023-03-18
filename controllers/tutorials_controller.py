from flask import Blueprint, jsonify, request, abort
from sqlalchemy import update
from main import db
from models.tutorials import Tutorial
from schemas.tutorial_schema import tutorial_schema, tutorials_schema
from controllers.auth_controller import authenticate_admin, authenticate_user, error_handler

tutorials = Blueprint('tutorials', __name__, url_prefix="/tutorials")

# Get all tutorials
@tutorials.route("/", methods=["GET"])
@error_handler
def get_tutorials():
    # get all tutorials from the database
    tutorials_list = Tutorial.query.all()
    # return data from database in JSON format
    result = tutorials_schema.dump(tutorials_list)
    return jsonify(result)


# Get tutorial by id
@tutorials.route("/<int:id>/", methods=["GET"])
@error_handler
def get_tutorial(id):
    # get tutorial with id from database
    tutorial = Tutorial.query.filter_by(id=id).first()
    result = tutorial_schema.dump(tutorial)
    return jsonify(result)


# Get all tutorials added by a user
@tutorials.route("/users/<int:user_id>", methods=["GET"])
@error_handler
def get_tutorial_by_user(user_id):
    # Get all tutorials with user id
    tutorials_list = Tutorial.query.filter_by(user_id=user_id)
    result = tutorials_schema.dump(tutorials_list)
    return jsonify(result)


# Get all tutorials by an author
@tutorials.route("authors/<string:author>", methods=["GET"])
@error_handler
def get_tutorial_by_author(author):
    tutorials_list = Tutorial.query.filter_by(author=author)
    result = tutorials_schema.dump(tutorials_list)
    return jsonify(result)


@tutorials.route("/", methods=["POST"])
@authenticate_user
@error_handler
def create_tutorial(**kwargs):
    user_id = kwargs["user_id"]
    # Create a new tutorial
    tutorial_fields = request.get_json()
    new_tutorial = Tutorial()
    # Loop through JSON and get fields
    for key, value in tutorial_fields.items():
        setattr(new_tutorial, key, value)
    new_tutorial.user_id = user_id
    db.session.add(new_tutorial)
    db.session.commit()
    return jsonify(tutorial_schema.dump(new_tutorial))


@tutorials.route("/<int:id>/edit", methods=["POST"])
@authenticate_user
@error_handler
def edit_tutorial(id, **kwargs):
    user_id = kwargs["user_id"]
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
@authenticate_user
@authenticate_admin
@error_handler
def delete_tutorial(id, **kwargs):
    # Find tutorial to be deleted
    tutorial = Tutorial.query.filter_by(id=id).first()
    # Tutorial does not exist
    if not tutorial:
        return abort(400, description="Tutorial does not exist")
    # Delete tutorial from database
    db.session.delete(tutorial)
    db.session.commit()
    return jsonify(tutorial_schema.dump(tutorial))