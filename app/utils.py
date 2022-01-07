from app import *
from app.models import *

# load phòng tất cả các phòng
def load_rooms(kind_of_room_id=None, page = 1):
    rooms = Room.query.filter(Room.active.__eq__(1))
    if kind_of_room_id:
        rooms = rooms.filter(Room.kind_of_room_id.__eq__(int(kind_of_room_id)))
    page_size = app.config['CUSTOMER_PAGE_SIZE']
    start = (page-1)*page_size
    end = start + page_size
    return rooms.slice(start, end).all()

# load 1 thể loại
def load_kind(kind_of_room_id):
    return KindOfRoom.query.get(kind_of_room_id)

# Lấy tất cả các ảnh theo thể loại
def get_kinds_images(kind_of_room_id=None):
    imgs = Image.query.all()
    if kind_of_room_id:
        imgs = Image.query.filter(Image.kind_of_room_id.__eq__(kind_of_room_id))
    return [x for x in imgs]


# Lấy tổng pages của 1 thể loại
def count_rooms(kind_of_room_id):
    return Room.query.filter(Room.kind_of_room_id.__eq__(kind_of_room_id)).count()
if __name__ == "__main__":
    # print(get_kinds_images())
    pass