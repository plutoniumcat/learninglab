from flask import Blueprint, jsonify, request
from main import db
from models.users import User

users = Blueprint('users', __name__, url_prefix="/users")

@users.route("/", methods=["GET"])
def get_users():
    # get all users from the database
    users_list = User.query.all()
    # return data from database in JSON format
    result = users_schema.dump(users_list)
    return jsonify(result)

@users.route("/", methods=["POST"])
def create_user():
    # Create a new user
    user_fields = user_schema.load(request.json)
    new_user = User()
    new_user.username = user_fields["username"]
    new_user.email = user_fields["email"]
    new_user.password = user_fields["password"]
    new_user.profile = user_fields["profile"]
    new_user.admin = user_fields["admin"]
    # add to database
    db.session.add(new_user)
    db.session.commit()
    return jsonify(user_schema.dump(new_user))

@users.route("/<int:id>/", methods=["DELETE"])
def delete_user():
    # Get ID of user who is attempting to delete
    user_id = get_jwt_identity()
    # Find user in database
    user = User.query.get(user_id)
    # Not a valid user
    if not user:
        return abort(401, description="Invalid user")
    if not user.admin:
        return abort(401, description="Not authorized to delete users")
    # Find user to be deleted
    user = User.query.filter_by(id=id).first()
    # User does not exist
    if not user:
        return abort(400, description="User does not exist")
    # Delete user from database
    db.session.delete(user)
    db.session.commit()
    return jsonify(user_schema.dump(user))