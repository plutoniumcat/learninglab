from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

def create_app():
    # create Flask app object
    app = Flask(__name__)

    # configure app
    app.config.from_object("config.app_config")

    # create database object
    db = SQLAlchemy(app)
    
    return app