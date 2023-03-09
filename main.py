# https://ait.instructure.com/courses/4487/assignments/49333
# https://blog.hubspot.com/website/api-endpoint
# https://api.cloudflare.com
# https://edstem.org/au/courses/10081/lessons/27621/slides/195167
# https://www.codementor.io/@sheena/understanding-sqlalchemy-cheat-sheet-du107lawl


from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
ma = Marshmallow()
bcrypt = Bcrypt()
jwt = JWTManager()

def create_app():
    # create Flask app object
    app = Flask(__name__)

    # configure app
    app.config.from_object("config.app_config")

    # create database object
    db.init_app(app)

    # create marshmallow object
    ma.init_app(app)

    # create bcrypt object
    bcrypt.init_app(app)

    #create jwt object
    jwt.init_app(app)

    # import and activate db commands
    from commands import db_commands
    app.register_blueprint(db_commands)

    # import controllers
    from controllers import registerable_controllers

    # activate blueprints
    for controller in registerable_controllers:
        app.register_blueprint(controller)
    
    return app