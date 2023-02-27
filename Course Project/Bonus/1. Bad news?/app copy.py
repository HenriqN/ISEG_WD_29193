from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import current_user, LoginManager

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///social_network.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.app_context().push()

login_manager = LoginManager()
login_manager.init_app(app)
@login_manager.user_loader

def load_user(user_id):
    return None

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    body = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

@app.route('/')
def index():
    return redirect(url_for('all_users'))

@app.route('/users')
def all_users():
    users = User.query.all()
    return render_template('all_users.html', users=users)

@app.route('/users/<int:user_id>')
def user_profile(user_id):
    user = User.query.get(user_id)
    posts = Post.query.filter_by(author_id=user_id).all()
    return render_template('user_profile.html', user=user, posts=posts)

@app.route('/posts/new', methods=['GET', 'POST'])
def new_post():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        author_id = current_user.id
        post = Post(title=title, body=body, author_id=author_id)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('user_profile', user_id=author_id))
    return render_template('new_post.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user:
            return render_template('register.html', error='Username already taken. Please choose another name.')
        new_user = User(username=username)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('all_users'))
    return render_template('register.html')

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username == "example_username" and password == "example_password":
            return "You have successfully logged in!"
        else:
            return "Incorrect username or password, please try again."
    return render_template("login.html")

if __name__ == "__main__":
    app.run(debug=True)

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)





