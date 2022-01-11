import datetime

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


# add rent room
def add_rent_room(rent_list):
    if 'rooms' in rent_list:
        rooms = rent_list.get('rooms')
        for room in rooms:
            if 'customers' in rooms[room]:
                customers = rooms[room]['customers']

                rent = Rent(check_in_date=rent_list['check_in_date'],
                            check_out_date=rent_list['check_out_date'],
                            room_id=rooms[room]['room_id'])

                for cus in customers:
                    customer = Customer.query.filter(
                        Customer.identification_card.__eq__(customers[cus]['identification_card'])).first()
                    if customer is None:
                        customer = customer = Customer(name=customers[cus]['name'],
                                                       identification_card=customers[cus]['identification_card'],
                                                       gender=customers[cus]['gender'],
                                                       customer_type_id=customers[cus]['customer_type_id'],
                                                       address=customers[cus]['address'],
                                                       phone_number=customers[cus]['phone_number'])
                        db.session.add(customer)
                    rent.customers.append(customer)
                db.session.add(rent)
        try:
            db.session.commit()
        except:
            return False
        return True
    return False


def load_book_room(identification_card=None,
                   check_from_in_date=None, check_to_in_date=None):
    # lay book room con hoat dong va chua nhan phong
    # lay book room khong con hoạt dong va da khong nhan phong
    book_rooms = BookRoom.query.filter(or_(and_(BookRoom.active.__eq__(True), BookRoom.done.__eq__(False)),
                                           and_(BookRoom.active.__eq__(False), BookRoom.done.__eq__(False))))

    if identification_card:
        # lay id customer
        cus = db.session.query(Customer.id).filter(Customer.identification_card.startswith(identification_card)).all()
        book_rooms = book_rooms.filter(BookRoom.customer_id.in_([x[0] for x in cus]))

    if check_from_in_date:
        book_rooms = book_rooms.filter(BookRoom.check_in_date.__le__(check_from_in_date))

    if check_to_in_date:
        book_rooms = book_rooms.filter(BookRoom.check_in_date.__ge__(check_to_in_date))

    return book_rooms.all()


if __name__ == '__main__':
    pass
