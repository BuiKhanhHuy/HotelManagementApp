import json
from app import app
from flask import render_template, request, redirect, url_for, jsonify, make_response, session
from app.admin import *
from app import dao, utils


@app.route("/")
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
@app.route("/employee/find-room", methods=['post'])
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
@app.route("/employee/add-to-book-room-cart", methods=['post'])
def add_to_book_room_cart():

    if 'book_room_list' not in session:
        session['book_room_list'] = {}
    book_room_list = session['book_room_list']

    # tao danh sach phong
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

    total_room = utils.total_room_in_book_room(room_list)
    return jsonify({'code': 200, 'total_room': total_room})

    # demo du lieu
    # book_room_list = {
    #     "customer": {
    #         'id': 1,
    #         'name': 'Huy'
    #     },
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
@app.route("/employee/book-room-detail")
def book_room_detail():
    return render_template('employee/book-room-detail.html')


# trang thue phong
@app.route("/employee/rent")
def rent():
    return render_template('employee/rent.html')


# trang thu phong truc tiep
@app.route("/employee/rent-directly")
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


# trang nhan phong da dat
@app.route("/employee/rent-advance")
def rent_advance():
    return render_template('employee/rent-advance.html')


# chi tiet thue phong
@app.route("/employee/rent-detail")
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

    }


if __name__ == "__main__":
    app.run(debug=True)
