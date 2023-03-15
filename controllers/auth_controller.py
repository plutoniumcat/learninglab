from flask import Blueprint, jsonify, request, abort
from functools import wraps
from main import db
from models.users import User
from schemas.user_schema import user_schema
from datetime import timedelta
from main import bcrypt
from flask_jwt_extended import create_access_token, verify_jwt_in_request, get_jwt_identity

auth = Blueprint('auth', __name__, url_prefix="/auth")

@auth.route("/register", methods=["POST"])
def auth_register():
    # Load request data into user schema
    user_fields = user_schema.load(request.json)
    # Check if user already exists
    user = User.query.filter_by(email=user_fields["email"]).first()
    if user:
        return abort(400, description="A user account with that email already exists.")
    # Create the user
    user = User()
    user.username = user_fields["username"]
    user.email = user_fields["email"]
    user.password = bcrypt.generate_password_hash(user_fields["password"]).decode("utf-8")
    user.admin = False
    # Add user to database
    db.session.add(user)
    db.session.commit()
    # Create expiry date for token
    expiry = timedelta(days=1)
    # Create access token
    access_token = create_access_token(identity=str(user.id), expires_delta=expiry)
    # Return user email and access token
    return jsonify({"user":user.email, "token": access_token })


@auth.route("login", methods=["POST"])
def auth_login():
    # Get user data from the request
    user_fields = user_schema.load(request.json)
    # Find user in database with email
    user = User.query.filter_by(email=user_fields["email"]).first()
    # If there is no user with that email, or the password is incorrect
    if not user or not bcrypt.check_password_hash(user.password, user_fields["password"]):
        return abort(401, description="Email or password is incorrect.")
    # Create expiry date for token
    expiry = timedelta(days=1)
    # Create access token
    access_token = create_access_token(identity=str(user.id), expires_delta=expiry)
    # Return user email and access token
    return jsonify({"user":user.email, "token": access_token })


# Decorator for other routes requiring user authentication
def authenticate_user(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        # Verify that user has JWT token
        verify_jwt_in_request()
        # Get user_id
        user_id = get_jwt_identity()
        # Find user in database
        user = User.query.get(user_id)
        # Not a valid user
        if not user:
            return abort(401, description="Invalid user")
        # Insert values into kwargs
        kwargs["user_id"] = user_id
        kwargs["user"] = user
        return f(*args, **kwargs)
    return decorator


def authenticate_admin(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        user = kwargs["user"]
        if not user.admin:
            return abort(401, description="Admin privileges required")
        return f(*args, **kwargs)
    return decorator