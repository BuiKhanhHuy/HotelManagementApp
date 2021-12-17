from app import db
from sqlalchemy import Column, Integer, String, DateTime, Float, Boolean, ForeignKey, Date
from sqlalchemy.orm import relationship, backref
from datetime import datetime
from flask_login import UserMixin


class BaseModel(db.Model):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)


class User(BaseModel, UserMixin):
    __tablename__ = 'user'
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(50), nullable=False)
    avatar = Column(String(50))
    email = Column(String(255), nullable=False, unique=True)
    active = Column(Boolean, default=True)
    joined_date = Column(DateTime, default=datetime.now())
    user_role_id = Column(Integer, ForeignKey('user_role.id'), default=3)
    comments = relationship('Comment', backref='user', lazy=True)

    def __str__(self):
        return self.username


class UserRole(BaseModel):
    __tablename__ = 'user_role'
    role_name = Column(String(50), nullable=False, unique=True)
    note = Column(String(255))
    users = relationship('User', backref='user_role', lazy=True)

    def __str__(self):
        return self.role_name


class Customer(BaseModel):
    __tablename__ = 'customer'
    first_name = Column(String(20), nullable=False)
    last_name = Column(String(50), nullable=False)
    birthday = Column(DateTime, nullable=False)
    gender = Column(String(20))
    identification_card = Column(Integer, nullable=False, unique=True)
    nationality = Column(String(100), nullable=False)
    address = Column(String(255), nullable=False)
    phone_number = Column(Integer, nullable=False)
    note = Column(String(255))
    comments = relationship('Comment', backref='customer', lazy=True)
    rents = relationship('Rent', backref='customer', lazy=True)
    book_rooms = relationship('BookRoom', backref='customer', lazy=True)

    def __str__(self):
        return "{0} {1}".format(self.last_name, self.first_name)


class KindOfRoom(BaseModel):
    __tablename__ = 'kind_of_room'
    kind_of_room_name = Column(String(100), nullable=False, unique=True)
    price = Column(Float, nullable=False)
    standard_number = Column(Integer, nullable=False)
    maximum_number = Column(Integer, nullable=False)
    image = Column(String(255), nullable=False)
    note = Column(String(255))
    rooms = relationship('Room', backref='kind_of_room', lazy=True)

    def __str__(self):
        return self.kind_of_room_name


class Room(BaseModel):
    __tablename__ = 'room'
    room_number = Column(Integer, nullable=False, unique=True)
    description = Column(String(1000), nullable=False)
    room_status_id = Column(Integer, ForeignKey('room_status.id'), nullable=False)
    kind_of_room_id = Column(Integer, ForeignKey('kind_of_room.id'), nullable=False)
    note = Column(String(255))
    comments = relationship('Comment', backref='room', lazy=True)
    images = relationship('Image', backref='room', lazy=True)

    def __str__(self):
        return str(self.room_number)


class RoomStatus(BaseModel):
    __tablename__ = 'room_status'
    room_status_name = Column(String(100), nullable=False, unique=True)
    note = Column(String(255))
    rooms = relationship('Room', backref='rooms_status', lazy=True)

    def __str__(self):
        return self.room_status_name


class Image(BaseModel):
    __tablename__ = 'image'
    link = Column(String(255), nullable=False)
    rank = Column(Integer, nullable=False)
    room_id = Column(Integer, ForeignKey('room.id'), nullable=False)
    note = Column(String(255))

    def __str__(self):
        return str(self.link)


class BookRoom(BaseModel):
    __tablename__ = 'book_room'
    check_in_date = Column(DateTime, nullable=False)
    check_out_date = Column(DateTime, nullable=False)
    customer_id = Column(Integer, ForeignKey('customer.id'), nullable=False)
    note = Column(String(255))
    rooms = relationship('Room', secondary='book_room_detail',
                         lazy='subquery', backref=backref('book_rooms', lazy=True))

    def __str__(self):
        return "Phiếu đặt phòng: {0} - {1}".format(self.check_in_date, self.check_out_date)


class Rent(BaseModel):
    __tablename__ = 'rent'
    check_in_date = Column(DateTime, nullable=False)
    check_out_date = Column(DateTime, nullable=False)
    customer_id = Column(Integer, ForeignKey('customer.id'), nullable=False)
    note = Column(String(255))
    bills = relationship('Bill', backref='rent', lazy=True)
    rooms = relationship('Room', secondary='rent_detail',
                         lazy='subquery', backref=backref('rents', lazy=True))

    def __str__(self):
        return "Phiếu thuê phòng: {0} - {1}".format(self.check_in_date, self.check_out_date)


class Bill(BaseModel):
    __tablename__ = 'bill'
    rent_id = Column(Integer, ForeignKey('rent.id'), nullable=False, unique=True)
    total = Column(Float, nullable=False)
    note = Column(String(255))

    def __str__(self):
        return "Mã hóa đơn {0}".format(self.id)


class Comment(db.Model):
    __tablename__ = 'comment'
    user_id = Column(Integer, ForeignKey('user.id'), primary_key=True, nullable=False)
    room_id = Column(Integer, ForeignKey('room.id'), primary_key=True, nullable=False)
    customer_id = Column(Integer, ForeignKey('customer.id'), nullable=False)
    created_date = Column(DateTime, default=datetime.now(), primary_key=True)
    content = Column(String(255), nullable=False)

    def __str__(self):
        return "{0}...".format(self.content[None:15])


class CommonCoefficient(BaseModel):
    __tablename__ = 'common_coefficient'
    check_in_deadline = Column(Integer, default=0)
    surcharge = Column(Float, default=1)
    number_foreign_visitor = Column(Float, default=1)


book_room_detail = db.Table('book_room_detail',
                            Column('book_room_id', Integer,
                                   ForeignKey('book_room.id'), primary_key=True),
                            Column('room_id', Integer,
                                   ForeignKey('room.id'), primary_key=True))


rent_detail = db.Table('rent_detail',
                       Column('rent_id', Integer,
                              ForeignKey('rent.id'), primary_key=True, nullable=False),
                       Column('room_id', Integer,
                              ForeignKey('room.id'), primary_key=True, nullable=False))


if __name__ == "__main__":
    pass
