# Import required libraries and modules
from flask import Blueprint, render_template, redirect, url_for, request, session
import models, views
import base64
from forms import LoginForm
from werkzeug.security import generate_password_hash, check_password_hash


bp = Blueprint("controller", __name__)  # Define a blueprint named "controller"
        
# Define a route for the index page        
@bp.route('/')
def index():
    return render_template('index.html')

# Define a route for submitting a comment
@bp.route('/comment', methods=['POST'])
def comment():
    form = LoginForm()  # Create a login form object
    # Get the post ID, user ID, and content from the form
    post_id = request.form.get('post_id')
    user = models.get_user(session.get('username'), "")
    if user:
        content = request.form.get('content')
        models.insert_comment(post_id, user[0], content)    # Insert the comment into the database
        # Get all the posts, comments and users from the database
        posts = models.get_posts()
        comments = models.get_comments()
        users = models.get_all_users()
        return render_template('feed.html', form = form, posts = posts, comments = comments, users = users)    #Render the feed template with the login form, posts, comments and users
    else:
        error = "You need to log in to comment"
        return render_template('login.html', form = form, error = error)

# Define a route for deleting a user profile page
@bp.route('/delete/<username>', methods=['GET', 'POST'])
def delete(username):
    form = LoginForm()
    user = models.get_user(str(username), "")   # Get the user object from the database, based on the given username
    # If the user is not found, return a 404 error
    if not user:
        return 'User not found', 404
    # If the request method is POST (i.e. a form has been submitted), process the form
    if request.method == 'POST':
        models.delete(user[0])
        session.pop('logged_in', None)
        session.pop('username', None)
    return redirect(url_for('controller.index'))

# Define a route for downvoting a comment
@bp.route('/downvote_comment', methods=['POST'])
def downvote_comment():
    form = LoginForm()  #Create a login form object
    comment_id = request.form.get('comment_id') # Get the comment ID from the form
    user = models.get_user(str(session.get('username')), "")    # Get the current user
    if user:
        models.downvote_comment(comment_id, user[0])    # Downvote the comment
        # Get all the posts, comments and users from the database
        posts = models.get_posts()
        comments = models.get_comments()
        users = models.get_all_users()
        return render_template('feed.html', posts = posts, form = form, comments = comments, users = users)    # Render the feed template with the login form, posts, comments and users
    else:
        error = "You need to log in to downvote a comment"
        return render_template('login.html', form = form, error = error)

# Define a route for downvoting a post
@bp.route('/downvote_post', methods=['POST'])
def downvote_post():
    form = LoginForm()  # Create a login form object
    post_id = request.form.get('post_id')   # Get the post ID from the form
    user = models.get_user(str(session.get('username')), "")    # Get the current user
    if user:
        models.downvote_post(post_id, user[0])  # Downvote the post
        # Get all the posts, comments and users from the database
        posts = models.get_posts()
        comments = models.get_comments()
        users = models.get_all_users()
        return render_template('feed.html', posts = posts, form = form, comments = comments, users = users)    # Render the feed template with the login form, posts, comments and users
    else:
        error = "You need to log in to downvote a post"
        return render_template('login.html', form = form, error = error)

# Define a route for the feed page
@bp.route('/feed')
def feed():
    # Get all the posts, comments, and users from the database
    posts = models.get_posts()
    comments = models.get_comments()
    users = models.get_all_users()
    form = LoginForm()  # Create a login form object
    return render_template('feed.html', posts = posts, form = form, comments = comments, users = users)   # Render the feed template with the login form, posts, comments, and users

# Define a route for the login page
@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    error = None
    # get the username or email and password from the request form
    if request.method == 'POST': 
        email_or_username = request.form['username']
        password = request.form['password']
        user = models.get_user(email_or_username, email_or_username)
        if user:
            if check_password_hash(user[3], password):
                session['logged_in'] = True
                session['username'] = user[1] if user[2] == email_or_username else email_or_username
                return redirect(url_for('controller.index'))
            else:
                error = 'Incorrect password'
        else:
            error = 'Username or email not found'
        return render_template('login.html', form = form, error = error)
    return render_template('login.html', form = form, error = error)

# Define a route for the logout page
@bp.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    return redirect(url_for('controller.index'))

# Define a route for the post page
@bp.route('/post', methods=['GET', 'POST'])
def post():
    form = LoginForm()
    posts = models.get_posts()
    comments = models.get_comments()
    users = models.get_all_users()
    # Check if the request method is POST, which indicates a form submission
    if request.method == 'POST':
        # Get the image and content from the request form
        image = request.files['image']
        image_bytes = image.read()
        img_b = base64.b64encode(image_bytes).decode('utf-8')   # Convert the image bytes to a base64-encoded string
        content = request.form['content']
        user = models.get_user(session.get('username'), "")
        if not user:
            error = "You need to log in to post"
            return render_template('login.html', form = form, error = error)
        models.insert_post(user[0], img_b , content)    # Insert the post into the database
        posts = models.get_posts()
        users = models.get_all_users()
        return render_template('feed.html', posts = posts, form = form, comments= comments, users = users)
    return render_template('feed.html', form = form, posts = posts, comments = comments, users = users)

# Define a route for the user profile page
@bp.route('/profile/<username>', methods=['GET', 'POST'])
def profile(username):
    form = LoginForm()
    user = models.get_user(str(username), "")   # Get the user object from the database, based on the given username
    # If the user is not found, return a 404 error
    if not user:
        return 'User not found', 404
    # Ff the request method is POST (i.e. a form has been submitted), process the form
    if request.method == 'POST':
        image = request.files['avatar'] # Get the uploaded image file from the request
        image_bytes = image.read()  # Read the file's contents into a byte string
        img_a = base64.b64encode(image_bytes).decode('utf-8')   # Convert the byte string to a base64-encoded string
        # If an image was uploaded, insert it into the database for the user
        if img_a != None:
            models.insert_avatar(user[0], img_a)
    # Get all the posts, comments and users from the database
    posts = models.get_user_posts(user[0])
    comments = models.get_comments()
    users = models.get_all_users()
    return render_template('user_profile.html', user = user, posts = posts, comments = comments, form = form, users = users)   # render the user profile page with the user's information, posts, comments and users

# Define a route for registering a new user
@bp.route('/register', methods=['GET', 'POST'])
def register():
    # If the request method is POST (i.e. a form has been submitted), process the form
    if request.method == 'POST':
        # Get the form data from the request
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        # Check that all fields were entered
        if not username or not email or not password or not confirm_password:
            return render_template('register.html', error='Please enter all fields')
        # Check that all fields are at least 3 characters long
        if len(username) < 3 or len(email) < 3 or len(password) < 3 or len(confirm_password) < 3:
            return render_template('register.html', error='Fields must be at least 3 characters long')     
        # Check that the two password fields match   
        if password != confirm_password:
            return render_template('register.html', error='Passwords must match')
        hashed_password = generate_password_hash(password, method='sha256') # Hash the password using SHA256
        # Check that no user with the same username or email exists
        user = models.get_user(username, email)
        if user:
            return render_template('register.html', error='Username or Email already exists')
        models.register_user(username, email, hashed_password)
        return redirect(url_for('controller.login'))
    return views.register()

# Define a route for search page that allows users to search for posts based on a search query
@bp.route('/search', methods=['GET', 'POST'])
def search():
    form = LoginForm()
    users = models.get_all_users()
    # If the request method is POST, retrieve the search query from the form data, 
    # call models.search() to retrieve a list of relevant posts, call models.get_comments() 
    # to retrieve all comments on the posts, and render the search.html template with the relevant data
    if request.method == 'POST':
        search_query = request.form['query']
        results = models.search(search_query)
        comments = models.get_comments()
        if not session.get('username'):
            return render_template('login.html', form = form) # If the user is not logged in, redirect to the login page
        return render_template('search.html', posts = results, search_query = search_query, form = form, comments = comments, users = users)    # If the user is logged in, render the search.html template with the relevant data
    else:
        return render_template('search.html',form = form)   # If the request method is not POST, simply render the search.html template with an empty form object

# Define a route for upvoting a comment
@bp.route('/upvote_comment', methods=['POST'])
def upvote_comment():
    form = LoginForm()
    comment_id = request.form.get('comment_id') # Extract the comment ID from the request data
    user = models.get_user(str(session.get('username')), "")    # Get the current user's information from the database
    if user:
        # Call models.upvote_comment() to update the database with the upvote and retrieve the updated posts and comments
        models.upvote_comment(comment_id, user[0])
        posts = models.get_posts()
        comments = models.get_comments()
        users = models.get_all_users()
        return render_template('feed.html', posts = posts, form = form, comments = comments, users = users)    # Render the feed.html template with the updated data
    else:
        error = "You need to log in to upvote a comment"
        return render_template('login.html', form = form, error = error)

# Define a route for upvoting a post
@bp.route('/upvote_post', methods=['POST'])
def upvote_post():
    form = LoginForm()
    post_id = request.form.get('post_id')   # Extract the post ID from the request data
    user = models.get_user(str(session.get('username')), "")    # Get the current user's information from the database
    if user:
        # Call models.upvote_post() to update the database with the upvote and retrieve the updated posts and comments
        models.upvote_post(post_id, user[0])
        posts = models.get_posts()
        comments = models.get_comments()
        users = models.get_all_users()
        return render_template('feed.html', posts = posts, form = form, comments = comments, users = users)    # Render the feed.html template with the updated data
    else:
        error = "You need to log in to upvote a post"
        return render_template('login.html', form = form, error = error)
    


    