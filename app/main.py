from app import app
import datetime
import schedule
import time
from flask import render_template, request, redirect, url_for, jsonify, session, flash
from app import dao, utils
from app.admin import *


@app.route("/")
@app.route("/home")
def index():
    del session['rent_directly_list']
    return render_template("home/index.html")


# ===================DAT PHONG==================


# trang dat phong
@app.route("/employee/book-room")
def book_room():
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
            flash('Bạn chưa chọn ngày nhận phòng!')
            return redirect(url_for('book_room'))

        if check_out_date:
            check_out_date = datetime.strptime(check_out_date, '%Y-%m-%d')
            check_out_date = check_out_date.replace(hour=12, minute=0, second=0)
        else:
            flash('Bạn chưa chọn ngày trả phòng!')
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
            flash('Bạn chưa chọn phòng để đặt!')
            return redirect(url_for('book_room'))
    return redirect(url_for('book_room'))


# ket qua dat phong
@app.route("/employee/book-room/<int:result>", methods=['get', 'post'])
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
            flash('Hủy đặt phòng thành công', category='info')
        return redirect(url_for('book_room_detail'))


# ===================END DAT PHONG==================


# ==========THUE PHONG TRUC TIEP====================


# trang thue phong
@app.route("/employee/rent")
def rent():
    return render_template('employee/rent.html')


# trang thue phong truc tiep
@app.route("/employee/rent/rent-directly")
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
def confirm_rental_directly_room():
    # phuong thuc post chuyen sang phong duoc thue
    if request.method.__eq__('POST'):
        check_in_date = request.form.get('check_in_date_rent_directly')
        check_out_date = request.form.get('check_out_date_rent_directly')

        if check_in_date:
            check_in_date = datetime.strptime(check_in_date, '%Y-%m-%d')
            check_in_date = check_in_date.replace(hour=14, minute=0, second=0)
        else:
            flash('Bạn chưa chọn ngày nhận phòng!')
            return redirect(url_for('rent_directly'))

        if check_out_date:
            check_out_date = datetime.strptime(check_out_date, '%Y-%m-%d')
            check_out_date = check_out_date.replace(hour=12, minute=0, second=0)
        else:
            flash('Bạn chưa chọn ngày trả phòng!')
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
            flash('Bạn chưa chọn phòng để thuê!')
            return redirect(url_for('rent_directly'))
    return redirect(url_for('rent_directly'))


# phan bo khach vao phong thue
@app.route("/employee/rent/rent-directly/allocating-customer")
def allocating_customers_rent_room():
    if 'rent_directly_list' in session and session['rent_directly_list'].__ne__({}):
        rent_directly_list = session['rent_directly_list']
        return render_template("employee/allocating-customers.html",
                               rent_directly_list=rent_directly_list)

    else:
        flash('Hiện tại chưa có phòng nào được chọn!')
    return redirect(url_for('rent_directly'))


# ket qua thue phong
@app.route("/employee/rent/result")
def rent_result():
    if 'rent_directly_list' in session:
        rent_directly_list = session['rent_directly_list']
        del session['rent_directly_list']

        if dao.add_rent_room(rent_directly_list):
            flash('Thêm phiếu thuê phòng thành công')
        else:
            flash('Thêm phiếu thuê phòng thất bại!')

        return render_template("employee/rent-print.html",
                               rent_directly_list=rent_directly_list)
    return redirect(url_for('rent_directly'))


# ==========END THUE PHONG TRUC TIEP================


# ================NHAN PHONG DA DAT==================


# trang nhan phong da dat
@app.route("/employee/rent/rent-advance")
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
def payment():
    return render_template('employee/payment.html')


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


# them khach hang vao ds phong thue truc tiep
@app.route("/api/employee/rent-directly/add-customer", methods=['post'])
def add_customer_to_directly():
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
    return jsonify({'code': code, 'room_id': room_id, 'customers': customers})


# tim phieu dat phong
@app.route("/api/employee/rent-advance/find-book-room", methods=['post'])
def find_book_room():
    data = request.json
    # CMND
    identification_card = data.get('identification_card')

    # ngay checkin
    check_from_in_date = data.get('check_from_in_date')
    if check_from_in_date.__ne__(''):
        check_from_in_date = datetime.strptime(check_from_in_date, '%Y-%m-%d')
        check_from_in_date = check_from_in_date.replace(hour=14, minute=0, second=0, microsecond=0)
    else:
        check_from_in_date = None

    # ngay check out
    check_to_in_date = data.get('check_to_in_date')
    if check_to_in_date.__ne__(''):
        check_to_in_date = datetime.strptime(check_to_in_date, '%Y-%m-%d')
        check_to_in_date = check_to_in_date.replace(hour=14, minute=0, second=0, microsecond=0)
    else:
        check_to_in_date = None

    # lay ngay hom nay
    today = datetime.now()
    today = today.replace(hour=14, minute=0, second=0, microsecond=0)

    # danh sach phong dat
    book_rooms = dao.load_book_room(identification_card=identification_card,
                                    check_from_in_date=check_from_in_date,
                                    check_to_in_date=check_to_in_date)
    book_room_list = []
    for b_room in book_rooms:
        room_numbers = [x.room_number for x in b_room.rooms]
        days = (today - b_room.check_in_date).days
        book_room_list.append({
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


# them khach hang vao ds phong nhan
@app.route("/api/employee/rent-advance/add-customer", methods=['post'])
def add_customer_to_advance():
    pass


# =====================END API==========================

# dang nhap
@app.route("/login")
def login_employee():
    return render_template('home/login.html')


# dang ky
@app.route("/register")
def register_employee():
    return render_template('home/register.html')


# loi 404
@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html')


# loi 401
@app.errorhandler(401)
def unauthorized(error):
    return render_template('401.html')


# loi 500
@app.errorhandler(500)
def internal_server_error(error):
    return render_template('500.html')


@app.context_processor
def common_response():
    return {
        'total_room_booking': utils.total_room_in_list(session.get('book_room_list')),
        'total_room_rent_directly': utils.total_room_in_list(session.get('rent_directly_list'))
    }


if __name__ == "__main__":
    app.run(debug=True)
