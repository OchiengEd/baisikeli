#!/usr/bin/env python3
from flask import Flask, render_template, redirect

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


@application.route('/strava/authorize')
def strava():
    return "Strava app authorization"
