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

@application.route('/user/signup', methods=['POST', 'GET'])
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

            print(user)
            # auth.create_user_account(user)

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
