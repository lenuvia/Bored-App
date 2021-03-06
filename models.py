"""SQLAlchemy models for Bored."""

from datetime import datetime
from enum import unique

from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
db = SQLAlchemy()


class User(db.Model):
    """User in the system."""

    __tablename__ = "users"

    id = db.Column(
        db.Integer,
        autoincrement=True,
        unique=True,
        primary_key=True,
    )

    email = db.Column(
        db.Text,
        nullable=False,
        unique=True,
    )

    username = db.Column(
        db.Text,
        nullable=False,
        unique=True,
    )

    password = db.Column(
        db.Text,
        nullable=False,
    )
    
    user_activities = db.relationship("User_Activity")
    ignored_activities= db.relationship("Ignored_Activity")


    def __repr__(self):
        return f"<User #{self.id}: {self.username}, {self.email}>"

    @classmethod
    def signup(cls, username, email, password):
        """Sign up user.

        Hashes password and adds user to system.
        """

        hashed_pwd = bcrypt.generate_password_hash(password).decode("UTF-8")

        user = User(
            username=username,
            email=email,
            password=hashed_pwd,
        )

        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, password):
        """Find user with `username` and `password`.

        This is a class method (call it on the class, not an individual user.)
        It searches for a user whose password hash matches this password
        and, if it finds such a user, returns that user object.

        If can't find matching user (or if password is wrong), returns False.
        """

        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False


class User_Activity(db.Model):
    """User Activities in the system."""

    __tablename__ = "user_activities"

    id = db.Column(
        db.Integer,
        autoincrement=True,
        primary_key=True,
        unique=True,
    )

    key = db.Column(
        db.Integer,
        unique=True,
    )

    title = db.Column(
        db.Text,
        nullable=False,
    )

    type = db.Column(
        db.Text,
        nullable=False,
    )

    participants = db.Column(
        db.Integer,
        default="1",
    )

    price = db.Column(
        db.Float,
        default="0.0",
    )
    
    timestamp = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow(),
    )
    
    isCompleted = db.Column(
        db.Boolean,
        default=False
    )
    
    note = db.Column(
        db.Text,
        nullable=True,
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="cascade"),
    )
    
    user= db.relationship("User")    

class Ignored_Activity(db.Model):
    """User ignored activities"""

    __tablename__ = "ignored_activities"

    id = db.Column(
        db.Integer,
        primary_key=True,
    )
    
    title = db.Column(
        db.Text,
        nullable=False,
    )
    
    key = db.Column(
        db.Integer,
        unique=True,
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="cascade"),
    )
    
    user= db.relationship("User")


def connect_db(app):
    """Connect db to app"""
    db.app = app
    db.init_app(app)
