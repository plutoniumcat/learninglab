from flask import Blueprint, jsonify, request
from main import db
from models.curriculum_associations import Association
from flask_jwt_extended import JWTManager, create_access_token, jwt_required

associations = Blueprint('associations', __name__, url_prefix="/associations")

@associations.route("/", methods=["GET"])
def get_associations():
    # get all associations from the database
    associations_list = Association.query.all()
    # return data from database in JSON format
    result = associations_schema.dump(associations_list)
    return jsonify(result)

@associations.route("/", methods=["POST"])
def create_association():
    # Create a new association
    association_fields = association_schema.load(request.json)
    new_association = Association()
    new_association.curriculum_id = association_fields["curriculum_id"]
    new_association.tutorial_id = association_fields["tutorial_id"]
    # add to database
    db.session.add(new_association)
    db.session.commit()
    return jsonify(association_schema.dump(new_association))

@associations.route("/<int:id>/", methods=["DELETE"])
def delete_association():
    # Get ID of user who is attempting to delete
    user_id = get_jwt_identity()
    # Find user in database
    user = User.query.get(user_id)
    # Not a valid user
    if not user:
        return abort(401, description="Invalid user")
    # TODO
        # Make so users can only delete own associations
    # Find association to be deleted
    association = Association.query.filter_by(id=id).first()
    # association does not exist
    if not association:
        return abort(400, description="Association does not exist")
    # Delete association from database
    db.session.delete(association)
    db.session.commit()
    return jsonify(association_schema.dump(association))