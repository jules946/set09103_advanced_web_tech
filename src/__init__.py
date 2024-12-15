from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os
from dotenv import load_dotenv

# create db and login_manager instances
db = SQLAlchemy()
login_manager = LoginManager()
load_dotenv()

def create_app():
    """
    Create a Flask application instance
    """
    # define the templates and static folders
    templates_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../templates')
    static_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../static')


    app = Flask(__name__, template_folder=templates_folder, static_folder=static_folder)
    # TODO: Set secret key properly
    app.config['SECRET_KEY'] = 'dev_secret_key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
    # disable modification tracking (saves memory)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # initialize db and login manager with app instance
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    # create database tables
    with app.app_context():
        db.create_all()

    # import User model
    from src.models import User

    # callback function to reload the user object
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # import and register blueprints
    from src.routes.auth import auth_bp
    from src.routes.main import main_bp
    from src.routes.players import players_bp
    from src.routes.search import search_bp
    from src.routes.teams import teams_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(main_bp)
    app.register_blueprint(players_bp)
    app.register_blueprint(search_bp)
    app.register_blueprint(teams_bp)

    return app