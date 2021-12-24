from app import app
from flask import render_template, request, redirect, url_for
from app.admin import *
from app.models import *


@app.route("/")
def index():
    return render_template("home/index.html")


@app.route("/employee/book-room")
def book_room():
    return render_template('employee/book-room.html')


@app.route("/employee/rent")
def rent():
    return render_template('employee/rent.html')


@app.route("/employee/rent-directly")
def rent_directly():
    return render_template('employee/rent-directly.html')


@app.route("/employee/rent-advance")
def rent_advance():
    return render_template('employee/rent-advance.html')


@app.route("/login")
def login_employee():
    return render_template('home/login.html')


@app.route("/register")
def register_employee():
    return render_template('home/register.html')


if __name__ == "__main__":
    app.run(debug=True)
