from flask import render_template


def index():
    return render_template("index.html")

def login():
    return render_template("login.html")

def register():
    return render_template("register.html")

def submit_post():
    return render_template("submit_post.html")
