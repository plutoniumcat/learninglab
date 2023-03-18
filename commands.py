from main import db
from flask import Blueprint
from main import bcrypt
from models.users import User
from models.tutorials import Tutorial
from models.curriculums import Curriculum
from models.curriculum_associations import Association

db_commands = Blueprint("db", __name__)

# CLI command "flask db create"
@db_commands .cli.command("create")
def create_db():
    db.create_all()
    print("Created all tables")


# CLI command "flask db seed"
@db_commands .cli.command("seed")
def seed_db():
    user1 = User(
        username = "TestAdmin",
        email = "testadmin@test.com",
        password = bcrypt.generate_password_hash("testpassword").decode("utf-8"),
        profile = "Hi, I'm a test user created to test the API.",
        admin = True
    )
    db.session.add(user1)
    
    user2 = User(
        username = "TestUser",
        email = "testuser@test.com",
        password = bcrypt.generate_password_hash("testpassword").decode("utf-8"),
        profile = "Hi, I'm a test user created to test the API.",
        admin = False
    )
    db.session.add(user2)
    db.session.commit()

    tutorial1 = Tutorial(
        url = "https://www.w3schools.com/python/python_intro.asp",
        user_id = user1.id,
        title = "Python Introduction",
        author = "W3Schools",
        description = "Introduction to coding in Python",
        level = "Beginner"
    )
    db.session.add(tutorial1)

    tutorial2 = Tutorial(
        url = "https://www.udemy.com/course/python-beyond-the-basics-object-oriented-programming/",
        user_id = user1.id,
        title = "Python Beyond the Basics - Object-Oriented Programming",
        author = "Infinite Skills",
        description = "From Classes To Inheritance - OOP In-Depth For Python Programmers",
        level = "Intermediate",
        pricing = 4299,
        length = "5h 1m"
    )
    db.session.add(tutorial2)
    db.session.commit()

    curriculum1 = Curriculum(
        user_id = user1.id,
        title = "Learning Python",
        description = "My Python journey"
    )
    db.session.add(curriculum1)
    db.session.commit()

    association1 = Association(
        curriculum_id = curriculum1.id,
        tutorial_id = tutorial1.id
    )
    db.session.add(association1)

    association2 = Association(
        curriculum_id = curriculum1.id,
        tutorial_id = tutorial2.id
    )
    db.session.add(association2)
    db.session.commit()
    print("Seeded all tables") 


# CLI command "flask db drop"
@db_commands .cli.command("drop")
def drop_db():
    db.drop_all()
    print("Dropped all tables") 