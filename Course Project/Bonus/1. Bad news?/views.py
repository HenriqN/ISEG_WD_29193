from flask import render_template

def index(error=None):
    return render_template('index.html', error=error)

def home(username):
    return render_template('home.html', username=username)