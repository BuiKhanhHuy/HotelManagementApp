from app.models import *
from sqlalchemy import func


# load rooms
def load_rooms(check_in_date=None, check_out_date=None,
               id_kind_of_room=None, price=None,
               max_people=None, room_number=None):
    rooms = Room.query.filter(Room.active.__eq__(True))

    if check_in_date and check_out_date:
        rooms = Room.query.filter(~Room.rents.any(and_(Rent.active.__eq__(True),
                                                       or_(and_(check_in_date >= Rent.check_in_date,
                                                                check_in_date <= Rent.check_out_date, ),
                                                           and_(check_out_date >= Rent.check_in_date,
                                                                check_out_date <= Rent.check_out_date),
                                                           and_(check_in_date <= Rent.check_in_date,
                                                                check_out_date >= Rent.check_out_date))))) \
            .filter(~Room.book_rooms.any(and_(BookRoom.active.__eq__(True),
                                              or_(and_(check_in_date >= BookRoom.check_in_date,
                                                       check_in_date <= BookRoom.check_out_date),
                                                  and_(check_out_date >= BookRoom.check_in_date,
                                                       check_out_date <= BookRoom.check_out_date),
                                                  and_(check_in_date <= BookRoom.check_in_date,
                                                       check_out_date >= BookRoom.check_out_date)))))
    if id_kind_of_room and id_kind_of_room.__ne__(0):
        rooms = rooms.filter(Room.kind_of_room_id.__eq__(id_kind_of_room))
    if price and price.__ne__(0):
        rooms = rooms.filter(Room.price.__lt__(price))
    if max_people and max_people.__ne__(0):
        rooms = rooms.filter(Room.maximum_number.__eq__(max_people))
    if room_number:
        rooms = rooms.filter(Room.room_number.startswith(room_number))

    return rooms.all()


# load kind of room
def load_kind_of_room():
    return KindOfRoom.query.all()


# max price
def max_price_of_room():
    max_price = db.session.query(func.max(Room.price)).first()
    return max_price


# maximum number of people in the room
def max_people_number_of_room():
    max_peoples = db.session.query(Room.maximum_number).distinct().all()
    return max_peoples


# load identification card
def find_identification_card(str_value):
    if str_value:
        return db.session.query(Customer.identification_card). \
            filter(Customer.identification_card.startswith(str_value)).all()


# load customer
def load_customers(identification_card=None):
    if identification_card:
        return Customer.query.filter(Customer.identification_card.__eq__(identification_card)).first()


# add book room
def add_book_room(name, gender, identification_card, customer_type_id,
                  phone_number, address, book_room_list, user=None):
    # them khach hang vao db
    customer = Customer.query.filter(Customer.identification_card.__eq__(identification_card.strip())).first()
    if customer is None:
        customer = Customer(name=name, identification_card=identification_card,
                            gender=gender, customer_type_id=customer_type_id,
                            address=address, phone_number=phone_number)
    db.session.add(customer)
    # # them phieu dat phong vao db
    booking_date = book_room_list.get('book_room_date')
    check_in_date = book_room_list.get('check_in_date')
    check_out_date = book_room_list.get('check_out_date')
    book_room = BookRoom(booking_date=booking_date, check_in_date=check_in_date, check_out_date=check_out_date,
                         customer=customer, user=user if user else None)
    db.session.add(book_room)

    # tạo phieu chi tiet dat phong
    rooms = book_room_list.get('rooms')
    for room in rooms:
        r = Room.query.get(rooms[room].get('room_id'))
        book_room.rooms.append(r)
        db.session.add(book_room)
    db.session.commit()


if __name__ == '__main__':
    # check_in_date = datetime.strptime('2022-01-07T14:00:00.000Z', '%Y-%m-%dT%H:%M:%S.%fZ')
    # check_out_date = datetime.strptime('2022-01-30T12:00:00.000Z', '%Y-%m-%dT%H:%M:%S.%fZ')
    #
    # # # lấy theo room
    # rooms = Room.query.filter(~Room.rents.any(and_(Rent.active.__eq__(True),
    #                                                or_(and_(check_in_date >= Rent.check_in_date,
    #                                                         check_in_date <= Rent.check_out_date, ),
    #                                                    and_(check_out_date >= Rent.check_in_date,
    #                                                         check_out_date <= Rent.check_out_date),
    #                                                    and_(check_in_date <= Rent.check_in_date,
    #                                                         check_out_date >= Rent.check_out_date))))) \
    #     .filter(~Room.book_rooms.any(and_(BookRoom.active.__eq__(True),
    #                                       or_(and_(check_in_date >= BookRoom.check_in_date,
    #                                                check_in_date <= BookRoom.check_out_date),
    #                                           and_(check_out_date >= BookRoom.check_in_date,
    #                                                check_out_date <= BookRoom.check_out_date),
    #                                           and_(check_in_date <= BookRoom.check_in_date,
    #                                                check_out_date >= BookRoom.check_out_date))))).all()
    #
    # print(rooms)
    pass
