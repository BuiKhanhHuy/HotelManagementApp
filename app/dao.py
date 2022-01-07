from app.models import *


# load rooms
def load_rooms():
    return Room.query.all()

# load nhiều thể loại
def load_kinds():
    return KindOfRoom.query.all()

# Lấy 1st ảnh theo thể loại
# def get_kinds_image():
    # kinds  = KindOfRoom.query.all()
    # list = []
    # for k in kinds:
    #     for x in k.images:
    #         if x.rank == 1:
    #             print(x.link)
    #
    # # return l
    #
    # lists =Image.query.filter()

if __name__ == "__main__":
    pass