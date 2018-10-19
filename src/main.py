#!/usr/bin/env python3
from flask import Flask, render_template, redirect, request
from baisikeli import Strava

application = Flask(__name__)

@application.route('/')
def index():
    return render_template('index.html')

@application.route('/auth/login')
def login():
    return "Login form"

@application.route('/admin/')
def admin():
    return "Admin page"


@application.route('/strava/authorization')
def strava_authorization():
    strava = Strava()
    access_token = strava.get_access_token(request.args.get('code'))
    if access_token is not None:
        return render_tamplate('connected.html')
