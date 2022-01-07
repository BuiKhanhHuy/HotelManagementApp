import datetime
import json
from app import app
from flask import render_template, request, redirect, url_for, jsonify, session, flash
from app.admin import *
from app import dao, utils


@app.route("/")
@app.route("/home")
def index():
    return render_template("home/index.html")


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

    total_room = utils.total_room_in_book_room(book_room_list)
    return jsonify({'code': 200, 'total_room': total_room})

    # demo du lieu dat phong
    # book_room_list = {
    #     "book_room_date": "today",
    #     "check_in_date": "01-01-2022",
    #     "check_ou_date": "05-01-2022",
    #     "rooms": {
    #         "id1": {
    #             'room_id': 1,
    #             'room_number': 101,
    #             'kind_of_room_name': 'standard',
    #             'price': 1000000,
    #             'image': 'anh.png'
    #         }
    #     }
    # }


# trang dat phong chi tiet
@app.route("/employee/book-room/book-room-detail", methods=['post', 'get'])
def book_room_detail():
    # phuong thuc post chuyen sang dat phong
    if request.method.__eq__('POST'):
        check_in_date = request.form.get('check_in_date_book_room')
        check_out_date = request.form.get('check_out_date_book_room')
        book_room_date = datetime.now()
        print(check_out_date)
        if check_in_date:
            check_in_date = datetime.strptime(
                str.format('{0} {1}', check_in_date, '14:00:00.0'),
                '%Y-%m-%d %H:%M:%S.%f')
        else:
            flash('Bạn chưa chọn ngày nhận phòng!')
            return redirect(url_for('book_room'))

        if check_out_date:
            check_out_date = datetime.strptime(
                str.format('{0} {1}', check_out_date, '12:00:00.0'),
                '%Y-%m-%d %H:%M:%S.%f')
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


# lay thong tin CMND duoc tim kiem tu client
@app.route("/api/employee/book-room/get-identification_card", methods=['post'])
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


# lay thong tin khach hang de hien thi thong tin dat phong
@app.route("/api/employee/book-room/get-customer", methods=['post'])
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
                    'total_room': utils.total_room_in_book_room(session['book_room_list']),
                    'room_numbers': room_numbers})


# in thong tin dat phong
@app.route("/employee/book-room/book-room-detail/<int:result>", methods=['get', 'post'])
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


# ==================================THUE PHONG TRUC TIEP=========================


# trang thue phong
@app.route("/employee/rent")
def rent():
    return render_template('employee/rent.html')


# trang thu phong truc tiep
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


# them phong vao cho dat phong
@app.route("/api/employee/rent-directly/add-to-rent-directly-cart", methods=['post'])
def add_to_rent_directly_cart():
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

    total_room = utils.total_room_in_book_room(book_room_list)
    return jsonify({'code': 200, 'total_room': total_room})

    # demo du lieu
    # rent_directly_list = {
    #     "check_in_date": "01-01-2022",
    #     "check_out_date": "05-01-2022",
    #     "rooms": {
    #         "id1": {
    #             'room_id': 1,
    #             'room_number': 101,
    #             'kind_of_room_name': 'standard',
    #             'price': 1000000,
    #             'image': 'anh.png',
    #             'customer': {
    #                   "name": 'Khanh Huy',
    #                   "address": 'Ben Tre'
    #              }
    #         }
    #     }
    # }


# ==================================NHAN PHONG DA DAT=========================


# trang nhan phong da dat
@app.route("/employee/rent/rent-advance")
def rent_advance():
    return render_template('employee/rent-advance.html')


# chi tiet thue phong
@app.route("/employee/rent/rent-detail")
def rent_detail():
    return 'rent_detail'


# trang thanh toan
@app.route("/employee/payment")
def payment():
    return render_template('employee/payment.html')


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
        'total_room_booking': utils.total_room_in_book_room(session.get('book_room_list'))
    }


if __name__ == "__main__":
    app.run(debug=True)
