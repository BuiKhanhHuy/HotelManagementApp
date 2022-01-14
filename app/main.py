import math

import cloudinary.uploader

from app import utils, dao, login
from flask import render_template, request, redirect, url_for
from flask_login import login_user, logout_user
from app.admin import *


# Customer Index
@app.route("/")
def index():
    kinds = dao.load_kinds()
    dic_image = dao.get_kinds_image()
    return render_template("home/index.html", kinds=kinds, dic_image=dic_image)


# liên hệ
@app.route("/contact")
def contact():
    return render_template("home/contact.html")


# About us
@app.route("/about-us")
def about_us():
    return render_template("home/about.html")


# Đặt phòng
@app.route("/booking")
def booking():
    kinds = dao.load_kinds()
    dic_image = dao.get_kinds_image()
    return render_template('home/rooms.html', kinds=kinds, dic_image=dic_image)


# Đặt phòng theo thể loại
@app.route("/booking/<int:kind_of_room_id>")
def booking_kinds(kind_of_room_id):
    page = int(request.args.get('page', 1))
    rooms = utils.load_rooms(kind_of_room_id=kind_of_room_id, page=page)
    kind = utils.load_kind(kind_of_room_id)
    imgs = utils.get_kinds_images(kind_of_room_id)
    counter = utils.count_rooms(kind_of_room_id)
    return render_template('home/bookingKind.html', rooms=rooms, kind=kind, imgs=imgs,
                           page=int(page), C_Pages=math.ceil(counter/app.config['CUSTOMER_PAGE_SIZE']))


# chi tiết đặt phòng
@app.route("/booking/room")
def room_detail():
    room_id = request.args.get("room_id")
    room = utils.load_rooms(room_id=room_id)
    return render_template('home/room_detail.html', room=room)


# Biểu mẫu đặt phòng
@app.route("/reservations")
def reservations():
    countries = dao.load_countries()
    return render_template('home/reservation.html', countries=countries)


# Đăng nhập người dùng
@app.route("/login", methods=['get', 'post'])
def customer_login():
    err_mgs = ""
    if request.method.__eq__('POST'):
        username = request.form.get('username')
        password = request.form.get('pass')

        user = utils.customer_login(username=username,
                                    password=password)
        if user:
            # ghi nhận user đã đăng nhập ; current_user toàn cục
            login_user(user=user)
            return redirect(url_for('index'))
        else:
            err_mgs = "Lỗi sai username hoặc password!!"
    return render_template('home/login.html', err_mgs=err_mgs)


# Đăng xuất người dùng
@app.route('/user-log-out')
def customer_sign_out():
    logout_user()
    return redirect(url_for('customer_login'))

# Đăng ký người dùng
@app.route("/register", methods=['get', 'post'])
def customer_register():
    err_mgs = ""
    if request.method.__eq__('POST'):
        username = request.form.get('username')
        password = request.form.get('password')
        confirm = request.form.get('confirm')
        email = request.form.get('email')
        avatar_path = None
        try:
            if password.strip().__eq__(confirm.strip()):
                avatar = request.files.get('avatar')
                if avatar:
                    res = cloudinary.uploader.upload(avatar)
                    avatar_path = res['secure_url']
                utils.add_customer_user(username=username,
                                        email=email,
                                        password=password,
                                        avatar=avatar_path)
                return redirect(url_for('customer_login'))
        except Exception as ex:
            err_mgs = "Lỗi:" + str(ex) + "!!"

    return render_template('home/register.html', err_mgs=err_mgs)


# tài khoản người dùng
@app.route("/account")
def load_profile_customer():
    return render_template('home/account.html')


# Load người dùng
@login.user_loader
def load_customer_user(user_id):
    return utils.get_customer_user_by_id(user_id=user_id)

# =============================Employee=============================
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
