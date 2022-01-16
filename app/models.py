from app import db
from sqlalchemy import Column, Integer, String, DateTime, Float, Enum, and_, or_, desc,\
    Boolean, ForeignKey
from sqlalchemy.orm import relationship, backref
from datetime import datetime
from flask_login import UserMixin
from enum import Enum as UserEnum


class UserRole(UserEnum):
    ADMIN = 1
    EMPLOYEE = 2
    USER = 3


class BaseModel(db.Model):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)


class User(BaseModel, UserMixin):
    __tablename__ = 'user'
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(50), nullable=False)
    avatar = Column(String(255))
    email = Column(String(255), nullable=False, unique=True)
    active = Column(Boolean, default=True)
    joined_date = Column(DateTime, default=datetime.now())
    user_role = Column(Enum(UserRole), default=UserRole.USER)
    comments = relationship('Comment', backref='user', lazy=True)
    book_rooms = relationship('BookRoom', backref='user', lazy=True)

    def __str__(self):
        return self.username


class CustomerType(BaseModel):
    __tablename__ = 'customer_type'
    customer_type_name = Column(String(30), nullable=False)
    note = Column(String(255))
    customers = relationship('Customer', backref='customer_type', lazy=True)

    def __str__(self):
        return self.customer_type_name


class Customer(BaseModel):
    __tablename__ = 'customer'
    name = Column(String(80), nullable=False)
    gender = Column(Boolean, default=True)
    identification_card = Column(String(20), nullable=False, unique=True)
    customer_type_id = Column(Integer, ForeignKey('customer_type.id'), nullable=False)
    address = Column(String(255), nullable=False)
    phone_number = Column(String(15), nullable=False)
    note = Column(String(255))
    book_rooms = relationship('BookRoom', backref='customer', lazy=True)

    def __str__(self):
        return self.name


class KindOfRoom(BaseModel):
    __tablename__ = 'kind_of_room'
    kind_of_room_name = Column(String(100), nullable=False, unique=True)
    description = Column(String(500), nullable=False)
    note = Column(String(255))
    images = relationship('Image', backref='kind_of_room', lazy=True)
    rooms = relationship('Room', backref='kind_of_room', lazy=True)

    def __str__(self):
        return self.kind_of_room_name


class RoomStatus(BaseModel):
    __tablename__ = 'room_status'
    room_status_name = Column(String(100), nullable=False)
    rooms = relationship('Room', backref='room_status', lazy=True)

    def __str__(self):
        return self.room_status_name


class Room(BaseModel):
    __tablename__ = 'room'
    room_number = Column(String(15), nullable=False, unique=True)
    price = Column(Float, nullable=False)
    standard_number = Column(Integer, default=2, nullable=False)
    maximum_number = Column(Integer, default=3, nullable=False)
    description = Column(String(1000), nullable=False)
    active = Column(Boolean, default=True)
    kind_of_room_id = Column(Integer, ForeignKey('kind_of_room.id'), nullable=False)
    room_status_id = Column(Integer, ForeignKey('room_status.id'), nullable=False)
    image = Column(String(255), nullable=False)
    note = Column(String(255))
    rents = relationship('Rent', backref='room', lazy=True)
    comments = relationship('Comment', backref='room', lazy=True)

    def __str__(self):
        return str(self.room_number)


class Image(BaseModel):
    __tablename__ = 'image'
    link = Column(String(255), nullable=False)
    rank = Column(Integer, nullable=False)
    kind_of_room_id = Column(Integer, ForeignKey('kind_of_room.id'), nullable=False)
    note = Column(String(255))

    def __str__(self):
        return str(self.link)


class BookRoom(BaseModel):
    __tablename__ = 'book_room'
    booking_date = Column(DateTime, default=datetime.now())
    check_in_date = Column(DateTime, nullable=False)
    check_out_date = Column(DateTime, nullable=False)
    active = Column(Boolean, default=True)
    done = Column(Boolean, default=False)
    note = Column(String(255))
    user_id = Column(Integer, ForeignKey('user.id'))
    customer_id = Column(Integer, ForeignKey('customer.id'), nullable=False)
    rooms = relationship('Room', secondary='book_room_detail',
                         lazy='subquery', backref=backref('book_rooms', lazy=True))

    def __str__(self):
        return "Phiếu đặt phòng: {0} - {1}".format(self.check_in_date, self.check_out_date)


class Rent(BaseModel):
    __tablename__ = 'rent'
    check_in_date = Column(DateTime, nullable=False)
    check_out_date = Column(DateTime, nullable=False)
    active = Column(Boolean, default=True)
    note = Column(String(255))
    room_id = Column(Integer, ForeignKey('room.id'), nullable=False)
    customers = relationship('Customer', secondary='rent_detail', lazy='subquery',
                             backref=backref('rents', lazy=True))
    bill = relationship('Bill', backref='rent', lazy=True)

    def __str__(self):
        return "Phiếu thuê phòng: {0} - {1}".format(self.check_in_date, self.check_out_date)


class Bill(BaseModel):
    __tablename__ = 'bill'
    total = Column(Float, nullable=False)
    note = Column(String(255))
    created_date = Column(DateTime, nullable=False)
    rent_id = Column(Integer, ForeignKey('rent.id'), nullable=False)

    def __str__(self):
        return "Mã hóa đơn {0}".format(self.id)


class Comment(BaseModel):
    __tablename__ = 'comment'
    user_id = Column(Integer, ForeignKey('user.id'), primary_key=True, nullable=False)
    room_id = Column(Integer, ForeignKey('room.id'), primary_key=True, nullable=False)
    created_date = Column(DateTime, default=datetime.now(), primary_key=True)
    content = Column(String(255), nullable=False)

    def __str__(self):
        return "{0}...".format(self.content[None:15])


class CommonCoefficient(BaseModel):
    __tablename__ = 'common_coefficient'
    check_in_deadline = Column(Integer, default=28)
    surcharge = Column(Float, default=0.25)
    number_foreign_visitor = Column(Float, default=1.5)


# book_room - room
book_room_detail = db.Table('book_room_detail',
                            Column('book_room_id', Integer,
                                   ForeignKey('book_room.id'), primary_key=True),
                            Column('room_id', Integer,
                                   ForeignKey('room.id'), primary_key=True))

# customer - rent
rent_detail = db.Table('rent_detail',
                       Column('rent_id', Integer,
                              ForeignKey('rent.id'), primary_key=True, nullable=False),
                       Column('customer_id', Integer,
                              ForeignKey('customer.id'), primary_key=True, nullable=False))


if __name__ == "__main__":
    # === DU LIEU BAT BUOC ===
    # Tinh trang phong: 1-Phong trong, 2-Phong da dat, 3-Phong dang thue
    # Loai khach: 1-Noi dia, 2-Nuoc ngoai
    # Tao he so chung
    db.create_all()
