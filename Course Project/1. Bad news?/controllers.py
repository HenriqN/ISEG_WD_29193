from flask import Blueprint, request, redirect, url_for, session
import views
import models

app = Blueprint('app', __name__)

@app.route('/')
def index_controller():
    if 'username' in session:
        return redirect(url_for('app.home_controller'))
    return views.index()

@app.route('/home', methods=['GET', 'POST'])
def home_controller():
    if request.method == 'POST':
        session.pop('username', None)
        return redirect(url_for('app.index_controller'))
    return views.home(session['username'])

@app.route('/login', methods=['GET', 'POST'])
def login_controller():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = models.get_user(username)
        if user is not None and user[1] == password:
            session['username'] = username
            return redirect(url_for('app.home_controller'))
        return views.index(error='Incorrect username or password')
    return redirect(url_for('app.index_controller'))

@app.route('/register', methods=['GET', 'POST'])
def register_controller():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = models.get_user(username)
        if user is None:
            models.add_user(username, password)
            return redirect(url_for('app.index_controller'))
        return views.index(error='Username already taken')
    return redirect(url_for('app.index_controller'))

