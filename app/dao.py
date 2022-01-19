import bdb
# import datetime
from datetime import timedelta
import hashlib
from app import app
from app.models import *
from sqlalchemy import func, extract
import pycountry
import copy


# =========CUSTOMER==========

# Lấy 1st ảnh theo thể loại
def get_kinds_image():
    kinds = KindOfRoom.query.all()
    dic = {}
    if kinds:
        for k in kinds:
            if k.images:
                for x in k.images:
                    if x.rank and x.rank.__eq__(1):
                        dic[k.id] = x.link
    return dic


def load_countries():
    return [p for p in pycountry.countries]


# =========EMPLOYEE==========


# load rooms
def load_rooms(check_in_date=None, check_out_date=None,
               id_kind_of_room=None, price=None,
               max_people=None, room_number=None, page=1):
    rooms = Room.query.filter(Room.active.__eq__(True))

    if check_in_date and check_out_date:
        rooms = rooms.filter(~Room.rents.any(and_(Rent.active.__eq__(True),
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

    page_size = app.config['EMPLOYEE_FIND_PAGE_SIZE']
    rooms = rooms.paginate(per_page=page_size, page=page)

    return rooms


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
        r.room_status_id = 2
        db.session.add(r)

        book_room.rooms.append(r)
        db.session.add(book_room)
    db.session.commit()


# add rent room
def add_rent_room(rent_list):
    if 'rooms' in rent_list:
        rooms = rent_list.get('rooms')
        for room in rooms:
            if 'customers' in rooms[room] and rooms[room]['customers'].__ne__({}):
                r = Room.query.get(rooms[room]['room_id'])
                r.room_status_id = 3
                db.session.add(r)

                customers = rooms[room]['customers']

                rent = Rent(check_in_date=rent_list['check_in_date'],
                            check_out_date=rent_list['check_out_date'],
                            room=r)

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


# load phieu thue phong tu ma thue phong
def load_book_room_from_id(book_room_id):
    return BookRoom.query.get(book_room_id)


# loc phieu thue phong
def load_book_room(identification_card=None,
                   check_in_date=None, check_out_date=None):
    # lay book room con hoat dong va chua nhan phong
    # lay book room khong con hoạt dong va da khong nhan phong
    book_rooms = BookRoom.query.filter(or_(and_(BookRoom.active.__eq__(True), BookRoom.done.__eq__(False)),
                                           and_(BookRoom.active.__eq__(False), BookRoom.done.__eq__(False))))
    if identification_card:
        # lay id customer
        cus = db.session.query(Customer.id).filter(Customer.identification_card.startswith(identification_card)).all()
        book_rooms = book_rooms.filter(BookRoom.customer_id.in_([x[0] for x in cus]))

    if check_in_date:
        book_rooms = book_rooms.filter(BookRoom.check_in_date.__eq__(check_in_date))

    if check_out_date:
        book_rooms = book_rooms.filter(BookRoom.check_out_date.__eq__(check_out_date))

    return book_rooms.all()


# hoan tat nhan phong
def successful_check_in(book_room_id):
    if book_room_id:
        book_room = BookRoom.query.get(book_room_id)
        book_room.done = True
        book_room.active = False
        db.session.add(book_room)
        try:
            db.session.commit()
        except:
            return False
    else:
        return False
    return True


# load common coefficient
def load_common_coefficient():
    return CommonCoefficient.query.first()


# kiem tra phieu thue co nguoi nuoc ngoai khong
def check_foreign(rent_id):
    if Customer.query.filter(Customer.rents.any(Rent.id == rent_id)).filter(
            Customer.customer_type_id == 2).count().__gt__(0):
        return True
    return False


# kiem tra phieu thue co so nguoi toi da hay khong
def check_people_max(rent_id, max_people):
    if Customer.query.filter(Customer.rents.any(Rent.id == rent_id)).count().__ge__(max_people):
        return True
    return False


# load rent
def load_rent(rent_id):
    return Rent.query.filter(Rent.id.__eq__(rent_id), Rent.active.__eq__(True)).first()


# payment
def payment(rent_id, today):
    total = 0
    common_coefficient = load_common_coefficient()

    rent = Rent.query.filter(Rent.id.__eq__(rent_id), Rent.active.__eq__(True)).first()
    if rent:
        room = Room.query.filter(Room.rents.any(Rent.id == rent_id)).first()

        price = room.price

        if check_foreign(rent_id):
            price = price * 1.5

        total += price * ((today - rent.check_in_date).days + 1)

        if check_people_max(rent_id, room.maximum_number):
            total += total * common_coefficient.surcharge

    return total


# load rent de thanh toan
def load_rent_payment(room_number=None, check_in_date=None, check_out_date=None):
    rent = Rent.query.filter(Rent.active.__eq__(True))

    if room_number:
        room_ids = db.session.query(Room.id).filter(Room.room_number.startswith(room_number)).all()
        rent = rent.filter(Rent.room_id.in_([x[0] for x in room_ids]))

    if check_in_date:
        rent = rent.filter(Rent.check_in_date.__eq__(check_in_date))

    if check_out_date:
        rent = rent.filter(Rent.check_out_date.__eq__(check_out_date))

    return rent.all()


# total bill waiting
def total_rent_waiting(active, today=None):
    rent = Rent.query.filter(Rent.active.__eq__(active))
    if today:
        rent = rent.filter(Rent.check_out_date < today)
    return rent.count()
    # return Rent.query.filter(Rent.active.__eq__(True)).count()


# total book room waiting
def total_book_room_waiting(active, done):
    # return BookRoom.query.filter(BookRoom.active.__eq__(True), BookRoom.done.__eq__(False)).count()
    return BookRoom.query.filter(BookRoom.active.__eq__(active), BookRoom.done.__eq__(done)).count()


# add bill
def add_bill(rent_id, total, today):
    rent = Rent.query.get(rent_id)
    if rent:
        rent.check_out_date = today
        db.session.add(rent)

        r = Room.query.filter(Room.rents.any(Rent.id.__eq__(rent_id))).first()
        r.room_status_id = 1
        db.session.add(r)

        rent.active = False
        db.session.add(rent)

        bill = Bill(total=total, rent=rent, created_date=today)
        db.session.add(bill)
        try:
            db.session.commit()
        except:
            return False
        else:
            return True
    return False


# thong ke doanh thu theo thang
def month_revenue_stats(year=None, month=None):
    stats = db.session.query(KindOfRoom.id, KindOfRoom.kind_of_room_name,
                             func.sum(Bill.total),
                             func.count(Rent.id)) \
        .join(Room, KindOfRoom.id.__eq__(Room.kind_of_room_id), isouter=True) \
        .join(Rent, Room.id.__eq__(Rent.room_id), isouter=True) \
        .join(Bill, Rent.id.__eq__(Bill.rent_id), isouter=True)

    if year:
        stats = stats.filter(extract('year', Bill.created_date).__eq__(year))

    if month:
        stats = stats.filter(extract('month', Bill.created_date).__eq__(month))

    stats = stats.group_by(KindOfRoom.id, KindOfRoom.kind_of_room_name).all()

    total = 0
    for x in stats:
        if x[2]:
            total += x[2]

    return stats, total


# thong ke mat do su dung phong
def month_density_stats(year=None, month=None):
    stats = db.session.query(Room.id, Room.room_number,
                             func.sum(func.date(Rent.check_out_date) - func.date(Rent.check_in_date))) \
        .join(Rent, Room.id.__eq__(Rent.room_id), isouter=True)

    if year:
        stats = stats.filter(extract('year', Rent.check_in_date).__eq__(year))
    if month:
        stats = stats.filter(extract('month', Rent.check_in_date).__eq__(month))
    stats = stats.group_by(Room.id, Room.room_number).all()

    total = 0
    for x in stats:
        if x[2]:
            total += x[2]

    return stats, total


# load user
def load_user(user_id):
    return User.query.get(user_id)


# check user
def check_user(user_name, password):
    if user_name and password:
        password = hashlib.md5(password.strip().encode('utf-8')).hexdigest()
        user = User.query.filter(User.username.__eq__(user_name.strip()), User.password.__eq__(password)).first()
        return user


# app comment
def add_comment(room_id, content, user_id):
    book_room = BookRoom.query.filter(BookRoom.rooms.any(Room.id.__eq__(room_id)),
                                      BookRoom.user_id.__eq__(user_id)).first()
    if book_room:
        comment = Comment(room_id=room_id, content=content, user_id=user_id)
        db.session.add(comment)
        try:
            db.session.commit()
        except:
            return None
        else:
            return Comment.query[-1]


# lay danh sach binh luan
def get_comment(room_id, page=1):
    comment_size = app.config['COMMENT_SIZE']
    return Comment.query.filter(Comment.room_id.__eq__(room_id)).paginate(per_page=comment_size, page=page)


if __name__ == '__main__':
    pass
