import hashlib
from app import app
from app import dao
from app.models import *


# ============CUSTOMER================
def check_user_exist(username=None, email=None):
    user = User.query
    count = 0
    if username:
        if user.filter(User.username.__eq__(username.strip())).first():
            return True

    if email:
        if user.filter(User.email.__eq__(email.strip())).first():
            return True
    return False


# Tạo user người dùng
def add_customer_user(username, email, password, **kwargs):
    password = str(hashlib.md5(password.strip().encode("utf-8")).hexdigest())
    new_user = User(username=username.strip(), email=email.strip(),
                    password=password, avatar=kwargs.get('avatar'))
    db.session.add(new_user)
    db.session.commit()


#    LOGIN USER
def customer_login(username, password):
    if username and password:
        password = str(hashlib.md5(password.strip().encode("utf-8")).hexdigest())

        return User.query.filter(User.username.__eq__(username.strip()),
                                 User.password.__eq__(password)).first()


# nạp customer user
def get_customer_user_by_id(user_id):
    return User.query.get(user_id)


# load phong tat ca phong
def load_rooms_of_customer(kind_of_room_id=None, check_in_date=None, check_out_date=None, page=1):
    # phan trang
    page_size = app.config['CUSTOMER_PAGE_SIZE']
    rooms = Room.query.filter(Room.active.__eq__(True))

    # filter theo dieu kien
    if kind_of_room_id and kind_of_room_id.__ne__(0):
        rooms = rooms.filter(Room.kind_of_room_id.__eq__(kind_of_room_id))

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

    rooms = rooms.paginate(per_page=page_size, page=page)
    return rooms


# load loai phong
def load_kinds(kind_of_room_id=None):
    kind_of_room = KindOfRoom.query
    if kind_of_room_id:
        kind_of_room.filter(KindOfRoom.id.__eq__(kind_of_room_id))
    return kind_of_room.all()


# load chi tiet phong
def load_room_detail(room_id):
    return Room.query.get(room_id)


# Lấy tất cả các ảnh theo thể loại
def get_kinds_images(kind_of_room_id=None):
    imgs = Image.query
    if kind_of_room_id:
        imgs = imgs.filter(Image.kind_of_room_id.__eq__(kind_of_room_id))
    return imgs.all()


# ============EMPLOYEE================

# all price options
def all_price_options():
    max_price = dao.max_price_of_room()
    if max_price:
        max_price = max_price[0]
        price_options = list()
        total = 0
        index = 1
        step = 1000000
        while total < max_price:
            total += index * step
            price_options.append(total)
            index += 1
        return price_options


# all maximum people options
def all_max_people_options():
    max_people_options = []
    for value in dao.max_people_number_of_room():
        max_people_options.append(value[0])
    return max_people_options


def total_room_in_list(room_list):
    if room_list and 'rooms' in room_list:
        return len(room_list.get('rooms').keys())
    return 0


if __name__ == '__main__':
    pass
