from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from ..models import db, User
from flask_login import login_user, logout_user, login_required, current_user

from ..services.balldontlie_api import BDLAPIService

# create a Blueprint for the auth routes
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    """
    Handle the signup route
    """
    # if the user submits the form
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # wrap database operations in application context
        with current_app.app_context():
            # check if the user already exists
            if User.query.filter_by(email=email).first():
                flash('Email is already registered. Please log in.', 'error')
                return redirect(url_for('auth.signup'))

            # check if the username is already taken
            if User.query.filter_by(username=username).first():
                flash('Username is already taken. Please choose another.', 'error')
                return redirect(url_for('auth.signup'))

            # create and store the user if the email and username are unique
            new_user = User(username=username, email=email)

            # hash and set the password
            new_user.set_password(password)

            # add the user to the database
            db.session.add(new_user)
            db.session.commit()

        flash('Account created successfully! Please log in.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('signup.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    Handle the login route
    """
    # if the user submits the form i.e. logs in
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # check if the user exists and the password is correct
        user = User.query.filter_by(email=email).first()
        # if login successful go back to home page
        if user and user.check_password(password):
            login_user(user)
            flash('Logged in successfully!', 'success')
            return redirect(url_for('main.index'))
        else:
            flash('Invalid email or password. Please try again.', 'error')

    return render_template('login.html')


@auth_bp.route('/logout')
@login_required
def logout():
    """
    Handle the logout route
    """
    # call flask_login logout_user function
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))


@auth_bp.route('/preferences', methods=['GET', 'POST'])
@login_required
def preferences():
    """
    Handle the user preferences route
    """
    api_service = BDLAPIService()

    if request.method == 'POST':
        favorite_team = request.form['team']
        favorite_player = request.form['player']

        with current_app.app_context():
            current_user.favorite_team = favorite_team
            current_user.favorite_player = favorite_player
            db.session.commit()

        flash('Preferences saved successfully!', 'success')
        return redirect(url_for('auth.preferences'))

    # Get teams and players from API
    teams = api_service.search_teams("")
    players = api_service.search_players("")

    return render_template('preferences.html', teams=teams, players=players)