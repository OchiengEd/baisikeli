#!/usr/bin/env python3
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import current_user, LoginManager, login_required, logout_user, login_user, UserMixin
from flask import Flask, render_template, redirect, request
from baisikeli import Strava
from model import Auth_Model

application = Flask(__name__)
login_manager = LoginManager(application)
strava = Strava()
auth = Auth_Model()

class User(UserMixin):

    def __init__(self):
        pass

    def __repr__(self):
        pass

@application.route('/')
def index():
    return render_template('index.html')

@application.route('/auth/login', methods=['POST', 'GET'])
def login():
    msg = None

    if request.method == 'POST':
        username = request.values.get('username')
        password = request.values.get('password')
        user = auth.authenticate_user(username)

        if check_password_hash(user['password'], password):
            return redirect('/admin')
        else:
            msg="An invalid username/password was used"

    return render_template('login.html', error=msg)

@application.route('/auth/logout')
def logout():
    logout_user()
    return redirect('/auth/login')

@application.route('/user/signup', methods=['POST'])
def create_user():
    if request.method == 'POST':

        if request.values.get('password1') == request.values.get('password2'):
            return render_template('signup.html', error="Passwords do not match!")
        elif request.values.get('email') == request.values.get('email_confirm'):
            return render_template('signup.html', error="Email addresses do not match!")

        user = {
            'first_name': request.values.get('firstname'),
            'last_name': request.values.get('lastname'),
            'email': request.values.get('email'),
            'password': generate_password_hash(request.values.get('password'))
            }

        if username is not None and password is not None:
            auth.create_user_account(user)

        return redirect('/auth/login')
    else:
        return render_template('signup.html')

@application.route('/admin/')
# @login_required
def admin():
    print(current_user.is_authenticated)
    return render_template('admin.html')

@application.route('/admin/connect')
def strava_connect():
    return redirect(strava.get_authorization_url())

@application.route('/strava/authorization')
def strava_authorization():
    access_token = strava.get_access_token(request.args.get('code'))
    if access_token is not None:
        return access_token
