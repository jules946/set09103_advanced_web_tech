from datetime import datetime, timezone

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
    password_hash = db.Column(db.String(256))
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


class NBAPlayer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    position = db.Column(db.String(50))
    height = db.Column(db.String(50))
    weight = db.Column(db.String(50))
    team_id = db.Column(db.Integer, db.ForeignKey('nba_team.id'))
    last_updated = db.Column(db.DateTime, default=datetime.now(timezone.utc))

    # relationship to team
    team = db.relationship('NBATeam', backref='players')


class NBATeam(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    full_name = db.Column(db.String(100))
    abbreviation = db.Column(db.String(10))
    city = db.Column(db.String(100))
    conference = db.Column(db.String(50))
    division = db.Column(db.String(50))
    last_updated = db.Column(db.DateTime, default=datetime.now(timezone.utc))


class PlayerStats(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey('nba_player.id'))
    season = db.Column(db.Integer)
    games_played = db.Column(db.Integer)
    pts = db.Column(db.Float)
    reb = db.Column(db.Float)
    ast = db.Column(db.Float)
    last_updated = db.Column(db.DateTime, default=datetime.now(timezone.utc))


class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime)
    home_team_id = db.Column(db.Integer, db.ForeignKey('nba_team.id'))
    visitor_team_id = db.Column(db.Integer, db.ForeignKey('nba_team.id'))
    home_team_score = db.Column(db.Integer, nullable=True)
    visitor_team_score = db.Column(db.Integer, nullable=True)
    status = db.Column(db.String(50))
    season = db.Column(db.Integer)
    last_updated = db.Column(db.DateTime, default=datetime.now(timezone.utc))

    # relationships to teams
    home_team = db.relationship('NBATeam', foreign_keys=[home_team_id])
    visitor_team = db.relationship('NBATeam', foreign_keys=[visitor_team_id])