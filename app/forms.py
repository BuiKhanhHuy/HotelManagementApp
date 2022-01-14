import cloudinary
from flask import request, redirect, url_for, render_template
from flask_login import login_user, logout_user
from app import dao, app, utils
from app.models import UserRole
from cloudinary import uploader


# dang nhap admin and employee
@app.route("/admin/login", methods=['post', 'get'])
def login_admin():
    if request.method.__eq__('POST'):
        user_name = request.form.get('user_name')
        password = request.form.get('password')

        user = dao.check_user(user_name, password)

        if user is None:
            return redirect(url_for('login_admin'))

        login_user(user=user)

        if user.user_role == UserRole.EMPLOYEE:
            next_page = url_for('dashboard')
        elif user.user_role == UserRole.ADMIN:
            next_page = '/admin'
        else:
            return redirect(url_for('login_admin'))

        if 'next' in request.args:
            next_page = request.args['next']

        return redirect(next_page)

    return render_template('employee/login.html')


# dang nhap nguoi dung
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


# dang xuat nguoi dung
@app.route('/user-log-out')
def customer_logout():
    logout_user()
    return redirect(url_for('customer_login'))


# dang xuat admin and emp
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login_admin'))
