from flask import Blueprint, jsonify, request, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import update
from main import db
from models.users import User
from schemas.user_schema import user_schema, users_schema

users = Blueprint('users', __name__, url_prefix="/users")

@users.route("/", methods=["GET"])
def get_users():
    # get all users from the database
    users_list = User.query.all()
    # return data from database in JSON format
    result = users_schema.dump(users_list)
    return jsonify(result)


@users.route("/<int:id>/", methods={"GET"})
def get_user(id):
    user = User.query.filter_by(id=id).first()
    result = user_schema.dump(user)
    return jsonify(result)


@users.route("/<int:id>/", methods=["POST"])
@jwt_required()
def update_profile(id):
    # Get ID of user who is attempting to edit
    user_id = get_jwt_identity()
    # Find user in database
    user = User.query.get(user_id)
    # Not a valid user
    if not user:
        return abort(401, description="Invalid user")
    # Not the owner of the profile
    elif int(user_id) != id:
        return abort(401, description="Not authorized to edit this user's profile")
    # Get profile data from request
    json_data = request.json
    new_profile = json_data['profile']
    update_profile = update(User).where(User.id==id).values(profile=new_profile)
    # Save to database
    db.session.execute(update_profile)
    db.session.commit()
    return {'message': 'Profile updated successfully'}


@users.route("/<int:id>/", methods=["DELETE"])
@jwt_required()
def delete_user(id):
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