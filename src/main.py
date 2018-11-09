#!/usr/bin/env python3
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import current_user, LoginManager, login_required, logout_user, login_user, UserMixin
from flask import Flask, render_template, redirect, request
from baisikeli import Strava
from model import Auth_Model
import os

application = Flask(__name__)
application.secret_key = os.urandom(24)
login_manager = LoginManager(application)
login_manager.login_view = '/auth/login'
strava = Strava()
auth = Auth_Model()

class User(UserMixin):

    def __init__(self, firstname, email):
        self.firstname = firstname
        self.email = email

    def __repr__(self):
        return '<{}:{}>'.format(self.firstname, self.email)

    def get_id(self):
        return str(self.email)

    def get_firstname(self):
        return self.firstname

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    @classmethod
    def get(cls, user_id):
        user = auth.get_user(user_id)
        return cls(user['firstname'], user['email'])


@application.route('/')
def index():
    return render_template('index.html')

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

@application.route('/auth/login', methods=['POST', 'GET'])
def login():
    msg = None

    if request.method == 'POST':
        email = request.values.get('email')
        password = request.values.get('password')
        user = auth.get_user(email)

        if check_password_hash(user['password'], password):
            authenticated_user = User(user['firstname'], user['email'])
            login_user(authenticated_user)

            return redirect('/admin')
        else:
            msg="An invalid username/password was used"

    return render_template('login.html', error=msg)

@application.route('/auth/logout')
def logout():
    logout_user()
    return redirect('/auth/login')

@application.route('/auth/signup', methods=['POST', 'GET'])
def create_user():
    warning = None

    if request.method == 'POST':

        if request.values.get('firstname') is not None and \
            request.values.get('password') is not None and \
            request.values.get('password') == request.values.get('password_confirm') and \
            request.values.get('email') == request.values.get('email_confirm'):

            user = {
            'firstname': request.values.get('firstname'),
            'lastname': request.values.get('lastname'),
            'email': request.values.get('email'),
            'password': generate_password_hash(request.values.get('password'))
            }

            auth.create_user_account(user)

            return redirect('/auth/login')

        elif request.values.get('password') != request.values.get('password_confirm'):

            warning = "Entered passwords not match"
            return render_template('signup.html', error=warning)

        elif request.values.get('email') != request.values.get('email_confirm'):

            warning = "Entered email addresses do not match"
            return render_template('signup.html', error=warning)
    else:
        return render_template('signup.html', error=warning)

@application.route('/admin/')
@login_required
def admin():
    return render_template('admin.html')

@application.route('/admin/connect')
def strava_connect():
    return redirect(strava.get_authorization_url())

@application.route('/strava/authorization')
def strava_authorization():
    access_token = strava.get_access_token(request.args.get('code'))
    if access_token is not None:
        return access_token
