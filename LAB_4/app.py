from flask import Flask, request, render_template
import sqlite3

app = Flask(__name__)

# @app.route("/")
# def hello():
#     return "Hello World!"

DATABASE = 'db.sqlite'

def connect_db():
    return sqlite3.connect(DATABASE)

# def init_db():
#     with connect_db() as con:
#         con.execute('CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT)')

def init_db():
    with connect_db() as con:
        con.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT)')

def create_user(name):
    with connect_db() as con:
        con.execute("INSERT INTO users (name) VALUES(?)", (name,))

def get_users():
    with connect_db() as con:
        cursor = con.execute("SELECT * FROM users")
        return cursor.fetchall()

def get_user(id):
    with connect_db() as con:
        cursor = con.execute("SELECT * FROM users WHERE id = ?", (id,))
        return cursor.fetchone()

def update_user(id, name):
    with connect_db() as con:
        con.execute("UPDATE users SET name = ? WHERE id = ?", (name, id))

def delete_user(id):
    with connect_db() as con:
        con.execute("DELETE FROM users WHERE id = ?", (id,))

@app.route("/")
def index():
    users = get_users()
    return render_template("index.html", users=users)

@app.route("/add_user", methods=["POST"])
def add_user():
    name = request.form.get("name")
    create_user(name)
    return "--- User " + name + " inserted into table users ---"

if __name__ == "__main__":
    init_db()
    app.run()

    