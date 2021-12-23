from app import app
from flask import render_template, request, redirect, url_for
from app.admin import *
from app.models import *


@app.route("/")
def index():
    return render_template('home/index.html')


@app.route("/login")
def login():
    return render_template('home/login.html')


@app.route("/register")
def register():
    return render_template('home/register.html')


if __name__ == "__main__":
    app.run(debug=True)
