from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from src import db


class User(UserMixin, db.Model):
    """
    User model for storing user information
    """
    __tablename__ = 'user'

    # define columns of User table
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    favorite_team = db.Column(db.Integer)
    favorite_player = db.Column(db.Integer)

    def set_password(self, password):
        """
        Hash password before storing it in the database
        """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """
        Check if the password matches the hashed password
        """
        return check_password_hash(self.password_hash, password)