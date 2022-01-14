from app import app
import datetime
from flask import render_template, request, redirect, url_for, jsonify, session, flash, abort
from flask_login import login_required, login_user, logout_user
from app import dao, utils, login
from app.admin import *

login.login_view = 'login_admin'


@app.route("/")
@app.route("/home")
def index():
    print(session.get('rent_advance_list'))
    print(session.get('rent_directly_list'))
    return render_template("home/index.html")


# ===================DAT PHONG==================


# trang danh sach phong
@app.route('/employee')
@login_required
def room_list():
    return 'Trang danh sách phòng'


# trang dat phong
@app.route("/employee/book-room")
@login_required
def book_room():
    if current_user.user_role.__ne__(UserRole.EMPLOYEE):
        return redirect(url_for('login_admin'))
    kind_of_rooms = dao.load_kind_of_room()
    rooms = dao.load_rooms()
    all_price_options = utils.all_price_options()
    all_max_people_options = utils.all_max_people_options()
    return render_template('employee/book-room.html',
                           kind_of_rooms=kind_of_rooms,
                           all_price_options=all_price_options,
                           all_max_people_options=all_max_people_options,
                           rooms=rooms)


# trang dat phong chi tiet
@app.route("/employee/book-room/book-room-detail", methods=['post', 'get'])
@login_required
def book_room_detail():
    # phuong thuc post chuyen sang dat phong
    if request.method.__eq__('POST'):
        check_in_date = request.form.get('check_in_date_book_room')
        check_out_date = request.form.get('check_out_date_book_room')
        book_room_date = datetime.now()
        if check_in_date:
            check_in_date = datetime.strptime(check_in_date, '%Y-%m-%d')
            check_in_date = check_in_date.replace(hour=14, minute=0, second=0)
        else:
            flash('Bạn chưa chọn ngày nhận phòng!', 'error')
            return redirect(url_for('book_room'))

        if check_out_date:
            check_out_date = datetime.strptime(check_out_date, '%Y-%m-%d')
            check_out_date = check_out_date.replace(hour=12, minute=0, second=0)
        else:
            flash('Bạn chưa chọn ngày trả phòng!', 'error')
            return redirect(url_for('book_room'))

        # load he so chung - 28 ngay
        common_coefficient = dao.load_common_coefficient()
        if (check_in_date - book_room_date).days > common_coefficient.check_in_deadline:
            flash('Ngày nhận phòng không quá {0} ngày kể từ ngày đặt phòng !'.format(
                common_coefficient.check_in_deadline), 'error')
            return redirect(url_for('book_room'))

        if 'book_room_list' in session and 'rooms' in session['book_room_list'] \
                and session['book_room_list']['rooms'].__ne__({}):
            book_room_list = session['book_room_list']
            book_room_list['check_in_date'] = check_in_date
            book_room_list['check_out_date'] = check_out_date
            book_room_list['book_room_date'] = book_room_date
            session['book_room_list'] = book_room_list
            book_room_list = session['book_room_list']

            rooms = []
            room_list = book_room_list['rooms']
            for room in room_list:
                rooms.append(room_list[room])
            return render_template('employee/book-room-detail.html', rooms=rooms,
                                   book_room_date=book_room_date.strftime("%d-%m-%Y"),
                                   check_in_date=check_in_date.strftime("%d-%m-%Y"),
                                   check_out_date=check_out_date.strftime("%d-%m-%Y"))
        else:
            flash('Bạn chưa chọn phòng để đặt!', 'error')
            return redirect(url_for('book_room'))
    return redirect(url_for('book_room'))


# ket qua dat phong
@app.route("/employee/book-room/<int:result>", methods=['get', 'post'])
@login_required
def booking_result(result):
    if result.__eq__(1):
        if request.method.__eq__('POST'):
            name_book_room = request.form.get('name_book_room')
            gender_book_room = request.form.get('gender_book_room')
            gender_book_room = eval(gender_book_room)
            id_card_book_room = request.form.get('id_card_book_room')
            cus_type_book_room = int(request.form.get('cus_type_book_room'))
            phone_book_room = request.form.get('phone_book_room')
            address_book_room = request.form.get('address_book_room')

            if 'book_room_list' in session:
                book_room_list = session.get('book_room_list')

                dao.add_book_room(name_book_room, gender_book_room, id_card_book_room,
                                  cus_type_book_room, phone_book_room, address_book_room, book_room_list)

                del session['book_room_list']

                return render_template('employee/book-room-print.html', book_room_list=book_room_list,
                                       name_book_room=name_book_room,
                                       cus_type_book_room=cus_type_book_room,
                                       id_card_book_room=id_card_book_room,
                                       address_book_room=address_book_room)

        return redirect(url_for('book_room_detail'))
    else:
        if 'book_room_list' in session:
            del session['book_room_list']
            flash('Hủy đặt phòng thành công.', 'success')
        return redirect(url_for('book_room_detail'))


# ===================END DAT PHONG==================


# ==========THUE PHONG TRUC TIEP====================


# trang thue phong
@app.route("/employee/rent")
@login_required
def rent():
    return render_template('employee/rent.html')


# trang thue phong truc tiep
@app.route("/employee/rent/rent-directly")
@login_required
def rent_directly():
    kind_of_rooms = dao.load_kind_of_room()
    rooms = dao.load_rooms()
    all_price_options = utils.all_price_options()
    all_max_people_options = utils.all_max_people_options()
    return render_template('employee/rent-directly.html',
                           kind_of_rooms=kind_of_rooms,
                           all_price_options=all_price_options,
                           all_max_people_options=all_max_people_options,
                           rooms=rooms)


# trang xac nhan phong thue truc tiep
@app.route("/employee/rent/rent-directly/confirm-room", methods=['get', 'post'])
@login_required
def confirm_rental_directly_room():
    # phuong thuc post chuyen sang phong duoc thue
    if request.method.__eq__('POST'):
        check_in_date = request.form.get('check_in_date_rent_directly')
        check_out_date = request.form.get('check_out_date_rent_directly')

        if check_in_date:
            check_in_date = datetime.strptime(check_in_date, '%Y-%m-%d')
            check_in_date = check_in_date.replace(hour=14, minute=0, second=0)
        else:
            flash('Bạn chưa chọn ngày nhận phòng!', 'error')
            return redirect(url_for('rent_directly'))

        if check_out_date:
            check_out_date = datetime.strptime(check_out_date, '%Y-%m-%d')
            check_out_date = check_out_date.replace(hour=12, minute=0, second=0)
        else:
            flash('Bạn chưa chọn ngày trả phòng!', 'error')
            return redirect(url_for('rent_directly'))

        if 'rent_directly_list' in session and 'rooms' in session['rent_directly_list'] \
                and session['rent_directly_list']['rooms'].__ne__({}):
            rent_directly_list = session['rent_directly_list']
            rent_directly_list['check_in_date'] = check_in_date
            rent_directly_list['check_out_date'] = check_out_date
            session['rent_directly_list'] = rent_directly_list
            rent_directly_list = session['rent_directly_list']

            rooms = []
            room_list = rent_directly_list['rooms']
            for room in room_list:
                rooms.append(room_list[room])
            return render_template('employee/confirm-rent-room.html', rooms=rooms,
                                   check_in_date=check_in_date.strftime("%d-%m-%Y"),
                                   check_out_date=check_out_date.strftime("%d-%m-%Y"))
        else:
            flash('Bạn chưa chọn phòng để thuê!', 'error')
            return redirect(url_for('rent_directly'))
    return redirect(url_for('rent_directly'))


# phan bo khach vao phong thue
@app.route("/employee/rent/allocating-customer/<int:allocating_customer_number>")
@login_required
def allocating_customers_rent_room(allocating_customer_number):
    # them khach hang vao session thue phong truc tiep
    if allocating_customer_number.__eq__(1):
        if 'rent_directly_list' in session and session['rent_directly_list'].__ne__({}):
            rent_directly_list = session['rent_directly_list']
            return render_template("employee/allocating-customers.html",
                                   allocating_customer_number=allocating_customer_number,
                                   rent_list=rent_directly_list)
        else:
            flash('Hiện tại chưa có phòng nào được chọn!', 'error')
        return redirect(url_for('rent_directly'))

    # them khach hang vao session nhan phong da dat
    elif allocating_customer_number.__eq__(2):

        if request.args.get('book_room_id'):
            book_room_id = int(request.args['book_room_id'])
            # lay phieu dat phong ra
            b_room = dao.load_book_room_from_id(book_room_id)

            if 'rent_advance_list' not in session:
                session['rent_advance_list'] = {}
            rent_advance_list = session['rent_advance_list'] = {}
            rent_advance_list['check_in_date'] = datetime.now().replace(hour=14, minute=0, second=0, microsecond=0)
            rent_advance_list['check_out_date'] = b_room.check_out_date
            rent_advance_list['book_room_id'] = book_room_id

            if 'rooms' not in rent_advance_list:
                rent_advance_list['rooms'] = {}
            rooms = rent_advance_list['rooms'] = {}

            for room in b_room.rooms:
                rooms[room.id] = {
                    'room_id': room.id,
                    'room_number': room.room_number,
                    'number_of_choose': room.maximum_number
                }

            rent_advance_list['rooms'] = rooms
            session['rent_advance_list'] = rent_advance_list

            return render_template("employee/allocating-customers.html",
                                   allocating_customer_number=allocating_customer_number,
                                   rent_list=rent_advance_list)
        else:
            flash('Bạn chưa chọn phiếu nhận phòng.', 'error')
            return redirect(url_for('rent_advance'))
    else:
        abort(404)
    return redirect(url_for('rent_advance'))


# ket qua thue phong
@app.route("/employee/rent/result/<int:result_number>")
@login_required
def rent_result(result_number):
    if result_number.__eq__(1):
        if 'rent_directly_list' in session:
            rent_directly_list = session['rent_directly_list']
            del session['rent_directly_list']

            if dao.add_rent_room(rent_directly_list):
                flash('Thêm phiếu thuê phòng thành công', 'success')
            else:
                flash('Thêm phiếu thuê phòng thất bại!', 'error')

            return render_template("employee/rent-print.html",
                                   rent_list=rent_directly_list)
        else:
            return redirect(url_for('rent_directly'))
    else:
        if result_number.__eq__(2):
            if 'rent_advance_list' in session:
                rent_advance_list = session['rent_advance_list']

                if dao.add_rent_room(rent_advance_list) \
                        and dao.successful_check_in(rent_advance_list['book_room_id']):
                    del session['rent_advance_list']
                    flash('Thêm phiếu thuê phòng thành công', 'success')
                else:
                    flash('Thêm phiếu thuê phòng thất bại!', 'error')

                return render_template("employee/rent-print.html",
                                       rent_list=rent_advance_list)
            else:
                return redirect(url_for('rent_advance'))
        else:
            abort(404)


# ==========END THUE PHONG TRUC TIEP================


# ================NHAN PHONG DA DAT==================


# trang nhan phong da dat
@app.route("/employee/rent/rent-advance")
@login_required
def rent_advance():
    book_rooms = dao.load_book_room()

    # lay ngay hom nay
    today = datetime.now()
    today = today.replace(hour=14, minute=0, second=0, microsecond=0)

    return render_template('employee/rent-advance.html',
                           book_rooms=book_rooms, today=today)


# ================END NHAN PHONG DA DAT==============


# ==================THANH TOAN=======================


# trang thanh toan
@app.route("/employee/payment")
@login_required
def payment():
    rents = dao.load_rent_payment()
    today = datetime.now()
    return render_template('employee/payment.html', rents=rents, today=today)


# trang thanh toan chi tiet
@app.route("/employee/payment-detail/<int:rent_id>")
@login_required
def payment_detail(rent_id):
    rent_room = dao.load_rent(rent_id)
    if rent_room:
        common_coefficient = dao.load_common_coefficient()
        check_foreign = dao.check_foreign(rent_id)
        check_people_max = dao.check_people_max(rent_id, rent_room.room.maximum_number)
        total = dao.payment(rent_id)

        return render_template("employee/payment-detail.html", rent_room=rent_room,
                               common_coefficient=common_coefficient,
                               check_foreign=check_foreign,
                               check_people_max=check_people_max,
                               total=total)
    abort(404)


# in phieu thanh toan
@app.route("/employee/payment/<int:rent_id>", methods=['post'])
@login_required
def payment_result(rent_id):
    if request.method.__eq__('POST'):
        rent_room = dao.load_rent(rent_id)
        if rent_room:
            name_pay = request.form.get('name_pay')
            total = dao.payment(rent_id=rent_id)

            if dao.add_bill(rent_id=rent_id, total=total):
                return render_template('employee/payment-print.html', rent_room=rent_room,
                                       name_pay=name_pay,
                                       total=total)
            else:
                flash('Xác nhận thanh toán không thành công!', 'error')
                return redirect(url_for('payment_detail'))
        else:
            flash('Xác nhận thanh toán không thành công!', 'error')
            return redirect(url_for('payment_detail'))

    return redirect(url_for('payment_detail'))


# ==================END THANH TOAN=======================


# =====================API==========================


# tim phong
@app.route("/api/employee/find-room", methods=['post'])
def find_room():
    data = request.json

    # du lieu tu giao dien
    check_in_date = datetime.strptime(data.get('check_in_date'), '%Y-%m-%dT%H:%M:%S.%fZ')
    check_out_date = datetime.strptime(data.get('check_out_date'), '%Y-%m-%dT%H:%M:%S.%fZ')
    id_kind_of_room = data.get('id_kind_of_room')
    price = data.get('price')
    max_people = data.get('max_people')
    room_number = data.get('room_number')

    # filter phong
    rooms = dao.load_rooms(check_in_date=check_in_date,
                           check_out_date=check_out_date,
                           id_kind_of_room=id_kind_of_room,
                           price=price, max_people=max_people,
                           room_number=room_number)

    room_list = []
    for room in rooms:
        room_list.append({
            'id': room.id,
            'image': room.image,
            'room_number': room.room_number,
            'maximum_number': room.maximum_number,
            'kind_of_room_name': room.kind_of_room.kind_of_room_name,
            'price': room.price,
            'description': room.description
        })

    return jsonify({'code': 200, 'rooms': room_list})


# lay thong tin CMND duoc tim kiem tu client
@app.route("/api/employee/get-identification_card", methods=['post'])
def get_id_card_book_room():
    data = request.json
    str_value = data.get('id_value')

    identification_cards = dao.find_identification_card(str_value)

    id_card_list = []
    for id_card in identification_cards:
        id_card_list.append({
            'label': str(id_card[0]),
            'value': str(id_card[0]),
        })
    return jsonify({'code': 200, 'identification_cards': id_card_list})


# lay thong tin khach hang de hien thi thong tin
@app.route("/api/employee/get-customer", methods=['post'])
def get_customer():
    data = request.json

    id_card = str(data.get('id_card'))

    customer = dao.load_customers(id_card)

    cus_dic = None
    if customer:
        cus_dic = {'id': customer.id, 'name': customer.name,
                   'gender': customer.gender, 'identification_card': customer.identification_card,
                   'address': customer.address, 'phone_number': customer.phone_number,
                   'customer_type_id': customer.customer_type.id}

    return jsonify({'code': 200, 'customer': cus_dic})


# xoa session dat phong
@app.route('/api/employee/book-room/clean-book-room', methods=['delete'])
def delete_book_room_session():
    code = 500
    if 'book_room_list' in session:
        del session['book_room_list']
        code = 200
    return {'code': code}


# xoa session thue phong
@app.route('/api/employee/rent-directly/clean-book-room', methods=['delete'])
def delete_rent_directly_session():
    code = 500
    if 'rent_directly_list' in session:
        del session['rent_directly_list']
        code = 200
    return {'code': code}


# them phong vao cho dat phong
@app.route("/api/employee/book-room/add-to-book-room-cart", methods=['post'])
def add_to_book_room_cart():
    if 'book_room_list' not in session:
        session['book_room_list'] = {}
    book_room_list = session['book_room_list']

    # tao danh sach phong
    if 'rooms' not in session['book_room_list']:
        book_room_list['rooms'] = {}
    room_list = book_room_list['rooms']

    # lay du lieu tu client
    data = request.json
    room_id = str(data.get('room_id'))
    room_number = data.get('room_number')
    kind_of_room_name = data.get('kind_of_room_name')
    price = data.get('price')
    image = data.get('image')

    # them hoac xoa phong o session
    if room_id in room_list:
        del room_list[room_id]
    else:
        room_list[room_id] = {
            'room_id': room_id,
            'room_number': room_number,
            'kind_of_room_name': kind_of_room_name,
            'price': price,
            'image': image
        }

    book_room_list['rooms'] = room_list
    session['book_room_list'] = book_room_list

    total_room = utils.total_room_in_list(book_room_list)
    return jsonify({'code': 200, 'total_room': total_room})


# xoa phong trong trang chi tiet dat phong
@app.route("/api/employee/book-room/delete-room/<int:room_id>", methods=['delete'])
def delete_room_in_book_room(room_id):
    room_id = str(room_id)
    room_numbers = []

    if 'book_room_list' in session:
        book_room_list = session['book_room_list']
        if 'rooms' in book_room_list:
            rooms = book_room_list['rooms']
            if room_id in rooms:
                del rooms[room_id]
                book_room_list['rooms'] = rooms
                session['book_room_list'] = book_room_list

                room_numbers = []
                for r in rooms:
                    room_numbers.append(rooms[r]['room_number'])

    return jsonify({'code': 200,
                    'total_room': utils.total_room_in_list(session['book_room_list']),
                    'room_numbers': room_numbers})


# them phong vao cho thue phong
@app.route("/api/employee/rent-directly/add-to-rent-directly-cart", methods=['post'])
def add_to_rent_directly_cart():
    if 'rent_directly_list' not in session:
        session['rent_directly_list'] = {}
    rent_directly_list = session['rent_directly_list']

    # tao danh sach phong
    if 'rooms' not in session['rent_directly_list']:
        rent_directly_list['rooms'] = {}
    room_list = rent_directly_list['rooms']

    # lay du lieu tu client
    data = request.json
    room_id = str(data.get('room_id'))
    room_number = data.get('room_number')
    kind_of_room_name = data.get('kind_of_room_name')
    price = data.get('price')
    image = data.get('image')
    maximum_number = data.get('maximum_number')

    # them hoac xoa phong o session
    if room_id in room_list:
        del room_list[room_id]
    else:
        room_list[room_id] = {
            'room_id': room_id,
            'room_number': room_number,
            'kind_of_room_name': kind_of_room_name,
            'price': price,
            'image': image,
            'maximum_number': maximum_number,
            'number_of_choose': maximum_number
        }
    rent_directly_list['rooms'] = room_list
    session['rent_directly_list'] = rent_directly_list
    print(session['rent_directly_list'])

    total_room = utils.total_room_in_list(rent_directly_list)
    return jsonify({'code': 200, 'total_room': total_room})


# xoa phong trong trang chi tiet dat phong
@app.route("/api/employee/rent-directly/delete-room/<int:room_id>", methods=['delete'])
def delete_room_in_rent(room_id):
    room_id = str(room_id)
    room_numbers = []

    if 'rent_directly_list' in session:
        rent_directly_list = session['rent_directly_list']
        if 'rooms' in rent_directly_list:
            rooms = rent_directly_list['rooms']
            if room_id in rooms:
                del rooms[room_id]
                rent_directly_list['rooms'] = rooms
                session['rent_directly_list'] = rent_directly_list

                room_numbers = []
                for r in rooms:
                    room_numbers.append(rooms[r]['room_number'])

    return jsonify({'code': 200,
                    'total_room': utils.total_room_in_list(session['rent_directly_list']),
                    'room_numbers': room_numbers})


# them khach hang vao ds phong thue
@app.route("/api/employee/add-customer/<int:add_customer_number>", methods=['post'])
def add_customer_to_rent(add_customer_number):
    data = request.json

    name = data.get('name')
    gender = int(data.get('gender'))
    customer_type_id = int(data.get('customer_type_id'))
    identification_card = data.get('identification_card')
    phone_number = data.get('phone_number')
    address = data.get('address')
    room_id = str(data.get('room_id'))
    number_of_choose = data.get('number_of_choose')

    code = 200
    customers = None

    # api them khach hang vao session thue truc tiep
    if add_customer_number.__eq__(1):
        if 'rent_directly_list' in session:
            rent_directly_list = session['rent_directly_list']
            if 'rooms' in rent_directly_list:
                rooms = rent_directly_list['rooms']
                if room_id in rooms:
                    rooms[room_id]['number_of_choose'] = number_of_choose
                    if 'customers' not in rooms[room_id]:
                        rooms[room_id]['customers'] = {}

                    customers = rooms[room_id]['customers']

                    customer_id = len(customers) + 1
                    customers[str(customer_id)] = {
                        'customer_id': customer_id,
                        'name': name,
                        'gender': gender,
                        'customer_type_id': customer_type_id,
                        'identification_card': identification_card,
                        'phone_number': phone_number,
                        'address': address
                    }
                    rooms[room_id]['customers'] = customers
                else:
                    code = 500
                rent_directly_list['rooms'] = rooms
            else:
                code = 500
            session['rent_directly_list'] = rent_directly_list
        else:
            code = 500
    # api them khach hang vao session nhan phong da dat
    else:
        if 'rent_advance_list' in session:
            rent_advance_list = session['rent_advance_list']
            if 'rooms' in rent_advance_list:
                rooms = rent_advance_list['rooms']
                if room_id in rooms:
                    rooms[room_id]['number_of_choose'] = number_of_choose
                    if 'customers' not in rooms[room_id]:
                        rooms[room_id]['customers'] = {}

                    customers = rooms[room_id]['customers']

                    customer_id = len(customers) + 1
                    customers[str(customer_id)] = {
                        'customer_id': customer_id,
                        'name': name,
                        'gender': gender,
                        'customer_type_id': customer_type_id,
                        'identification_card': identification_card,
                        'phone_number': phone_number,
                        'address': address
                    }
                    rooms[room_id]['customers'] = customers
                else:
                    code = 500
                rent_advance_list['rooms'] = rooms
            else:
                code = 500
            session['rent_advance_list'] = rent_advance_list
        else:
            code = 500
    return jsonify({'code': code, 'room_id': room_id, 'customers': customers})


# tim phieu dat phong
@app.route("/api/employee/rent-advance/find-book-room", methods=['post'])
def find_book_room():
    data = request.json
    # CMND
    identification_card = data.get('identification_card')

    # ngay checkin
    check_in_date = data.get('check_in_date')
    if check_in_date.__ne__(''):
        check_in_date = datetime.strptime(check_in_date, '%Y-%m-%d')
        check_in_date = check_in_date.replace(hour=14, minute=0, second=0, microsecond=0)
    else:
        check_in_date = None

    # ngay check out
    check_out_date = data.get('check_out_date')
    if check_out_date.__ne__(''):
        check_out_date = datetime.strptime(check_out_date, '%Y-%m-%d')
        check_out_date = check_out_date.replace(hour=12, minute=0, second=0, microsecond=0)
    else:
        check_out_date = None

    # lay ngay hom nay
    today = datetime.now()
    today = today.replace(hour=14, minute=0, second=0, microsecond=0)

    # danh sach phong dat
    book_rooms = dao.load_book_room(identification_card=identification_card,
                                    check_in_date=check_in_date,
                                    check_out_date=check_out_date)
    book_room_list = []
    for b_room in book_rooms:
        room_numbers = [x.room_number for x in b_room.rooms]
        days = (today - b_room.check_in_date).days
        book_room_list.append({
            'book_room_id': b_room.id,
            'booking_date': b_room.booking_date.strftime('%d-%m-%Y'),
            'check_in_date': b_room.check_in_date.strftime('%d-%m-%Y'),
            'check_out_date': b_room.check_out_date.strftime('%d-%m-%Y'),
            'customer_name': b_room.customer.name,
            'identification_card': b_room.customer.identification_card,
            'room_numbers': room_numbers,
            'active': b_room.active,
            'done': b_room.done,
            'days': days
        })

    return jsonify({'code': 200, 'book_room_list': book_room_list})


# tat hoat dong cua phieu dat phong het han
@app.route("/api/employee/rent-advance/inactive-book-room/<int:book_room_id>", methods=['delete'])
def inactive_book_room(book_room_id):
    code = 500
    if dao.successful_check_in(book_room_id):
        code = 200

    return jsonify({'code': code})


# tim phieu thue phong de thanh toan
@app.route("/api/employee/payment/find-rent", methods=['post'])
def find_rent_payment():
    data = request.json

    # so phong
    room_number = data.get('room_number')

    # ngay checkin
    check_in_date = data.get('check_in_date')
    if check_in_date.__ne__(''):
        check_in_date = datetime.strptime(check_in_date, '%Y-%m-%d')
        check_in_date = check_in_date.replace(hour=14, minute=0, second=0, microsecond=0)
    else:
        check_in_date = None

    # ngay check out
    check_out_date = data.get('check_out_date')
    if check_out_date.__ne__(''):
        check_out_date = datetime.strptime(check_out_date, '%Y-%m-%d')
        check_out_date = check_out_date.replace(hour=12, minute=0, second=0, microsecond=0)
    else:
        check_out_date = None

    rents = dao.load_rent_payment(room_number=room_number,
                                  check_in_date=check_in_date,
                                  check_out_date=check_out_date)
    rent_list = []
    for r in rents:
        rent_list.append({
            'rent_id': r.id,
            'check_in_date': r.check_in_date.strftime('%d-%m-%Y'),
            'check_out_date': r.check_out_date.strftime('%d-%m-%Y'),
            'room_number': r.room.room_number
        })

    return jsonify({'code': 200, 'rent_list': rent_list})


# =====================END API==========================


# dang nhap
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
            next_page = url_for('room_list')
        elif user.user_role == UserRole.ADMIN:
            next_page = '/admin'
        else:
            return redirect(url_for('login_admin'))

        if 'next' in request.args:
            next_page = request.args['next']

        return redirect(next_page)

    return render_template('employee/login.html')


# dang xuat
@app.route("/logout", methods=['post', 'get'])
def logout():
    logout_user()
    return redirect(url_for('login_admin'))


# loi 404
@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html')


# loi 405
@app.errorhandler(405)
def page_not_found(error):
    return render_template('405.html')


# loi 401
@app.errorhandler(401)
def unauthorized(error):
    return render_template('401.html')


# loi 500
@app.errorhandler(500)
def internal_server_error(error):
    return render_template('500.html')


@login.user_loader
def load_user(user_id):
    return dao.load_user(user_id)


@app.context_processor
def common_response():
    return {
        'total_room_booking': utils.total_room_in_list(session.get('book_room_list')),
        'total_room_rent_directly': utils.total_room_in_list(session.get('rent_directly_list')),
        'total_rent_waiting': dao.total_rent_waiting(),
        'total_book_room_waiting': dao.total_book_room_waiting()
    }


if __name__ == "__main__":
    app.run(debug=True)
