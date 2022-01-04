import json
from app import app
from flask import render_template, request, redirect, url_for, jsonify, make_response
from app.admin import *
from app import dao, utils


@app.route("/")
def index():
    return render_template("home/index.html")


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


@app.route("/employee/book-room-detail")
def book_room_detail():
    return render_template('employee/book-room-detail.html')


@app.route("/employee/rent")
def rent():
    return render_template('employee/rent.html')


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


@app.route("/employee/rent-advance")
def rent_advance():
    return render_template('employee/rent-advance.html')


@app.route("/employee/rent-detail")
def rent_detail():
    return 'rent_detail'


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
