#!/usr/bin/env python3
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, render_template, redirect, request
from baisikeli import Strava
from model import Auth_Model

application = Flask(__name__)
strava = Strava()
auth = Auth_Model()

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

@application.route('/user/signup', methods=['POST'])
def create_user():
    if request.method == 'POST':
        user = {
            'first_name': request.values.get('first_name'),
            'last_name': request.values.get('last_name'),
            'email': request.values.get('email'),
            'username': request.values.get('username'),
            'password': generate_password_hash(request.values.get('password'))
            }

        if username is not None and password is not None:
            auth.create_user_account(user)

        return redirect('/auth/login')
    else:
        return render_template('signup.html')

@application.route('/admin/')
def admin():
    return "Admin page"

@application.route('/admin/connect')
def strava_connect():
    return redirect(strava.get_authorization_url())

@application.route('/strava/authorization')
def strava_authorization():
    access_token = strava.get_access_token(request.args.get('code'))
    if access_token is not None:
        return access_token
