from app import app
from flask import render_template, request, redirect, url_for
from app.admin import *
from app import dao


@app.route("/")
def index():
    return render_template("home/index.html")


@app.route("/employee/book-room")
def book_room():
    rooms = dao.load_rooms()
    return render_template('employee/book-room.html', rooms=rooms)


@app.route("/employee/book-room/book-room-detail")
def book_room_detail():
    return render_template('employee/book-room-detail.html')


@app.route("/employee/rent")
def rent():
    return render_template('employee/rent.html')


@app.route("/employee/rent-directly")
def rent_directly():
    return render_template('employee/rent-directly.html')


@app.route("/employee/rent-advance")
def rent_advance():
    return render_template('employee/rent-advance.html')


@app.route("/employee/payment")
def payment():
    return render_template('employee/payment.html')


@app.route("/login")
def login_employee():
    return render_template('home/login.html')


@app.route("/register")
def register_employee():
    return render_template('home/register.html')


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html')


@app.errorhandler(401)
def unauthorized(error):
    return render_template('401.html')


@app.errorhandler(500)
def internal_server_error(error):
    return render_template('500.html')


if __name__ == "__main__":
    app.run(debug=True)
