from flask import Flask, request, make_response, render_template

app = Flask(__name__)

# @app.route('/')
# def index():
#     return 'Hello World!'

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

if __name__ == '__main__':
    app.run()

    