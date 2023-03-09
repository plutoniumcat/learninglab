from flask import Blueprint, jsonify, request
from main import db
from models.tutorials import Tutorial

tutorials = Blueprint('tutorials', __name__, url_prefix="/tutorials")

@tutorials.route("/", methods=["GET"])
def get_tutorials():
    # get all tutorials from the database
    tutorials_list = Tutorial.query.all()
    # return data from database in JSON format
    result = tutorials_schema.dump(tutorials_list)
    return jsonify(result)

@tutorials.route("/", methods=["POST"])
def create_tutorial():
    # Create a new tutorial
    tutorial_fields = tutorial_schema.load(request.json)
    new_tutorial = Tutorial()
    new_tutorial.url = tutorial_fields["url"]
    new_tutorial.user_id = tutorial_fields["user_id"]
    new_tutorial.title = tutorial_fields["title"]
    new_tutorial.author = tutorial_fields["author"]
    new_tutorial.description = tutorial_fields["description"]
    new_tutorial.level = tutorial_fields["level"]
    new_tutorial.prerequisites = tutorial_fields["prerequisites"]
    new_tutorial.pricing = tutorial_fields["pricing"]
    new_tutorial.length = tutorial_fields["length"]
    # add to database
    db.session.add(new_tutorial)
    db.session.commit()
    return jsonify(tutorial_schema.dump(new_tutorial))

@tutorials.route("/<int:id>/", methods=["DELETE"])
def delete_tutorial():
    # Get ID of user who is attempting to delete
    user_id = get_jwt_identity()
    # Find user in database
    user = User.query.get(user_id)
    # Not a valid user
    if not user:
        return abort(401, description="Invalid user")
    if not user.admin:
        return abort(401, description="Not authorized to delete users")
    # Find tutorial to be deleted
    tutorial = Tutorial.query.filter_by(id=id).first()
    # Tutorial does not exist
    if not tutorial:
        return abort(400, description="Tutorial does not exist")
    # Delete tutorial from database
    db.session.delete(tutorial)
    db.session.commit()
    return jsonify(tutorial_schema.dump(tutorial))