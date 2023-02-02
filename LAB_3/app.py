from flask import Flask, request, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)

# @app.route('/')
# def index():
#     return 'Hello World!!!'

@app.route('/users/<username>')
def show_user(username):
    return f'User: {username}'

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#    if request.method == 'POST': 
#        #handle login logic
#    else:
#        #show login form

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username'] 
    password = request.form['password'] 
    # handle login logic

# @app.route('/')
# def index():
#     response = make_response('Hello World!')
#     response.headers['Content-Type'] = 'text/plain'
#     return response

@app.route('/')
def index():
    name = 'John'
    return render_template('index.html', name=name)

# @app.route("/form", methods=["GET", "POST"])
# def form():
#     if request.method == "POST":
#         name = request.form["name"]
#         return "Hello " + name
#     return render_template("form.html")

class NameForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    submit = SubmitField("Submit")

@app.route("/form", methods=["GET", "POST"])
def form():
    form = NameForm()
    if request.method == "POST" and form.validate_on_submit():
        name = form.name.data
        return "Hello " + name
    return render_template("form.html", form=form)

app.config["SECRET_KEY"] = "abc"
csrf = CSRFProtect(app)


if __name__ == '__main__':
    app.run()
