# Import required libraries and modules
from flask import Flask
import controllers, models
import os
from flask_wtf.csrf import CSRFProtect


app = Flask(__name__)   # Create a Flask app instance
app.secret_key = os.urandom(24) # Set a secret key for the app to enable session management
CSRFProtect(app)    # Add CSRF protection to the app

app.register_blueprint(controllers.bp)  # Register the blueprint defined in the controllers module

# If this file is run as the main program, initialize the database and start the app with debug mode turned off
if __name__ == '__main__':
    models.init_db()
    app.run(debug=False)


