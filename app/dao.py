from app.models import *
import pycountry

# load rooms
def load_rooms():
    return Room.query.all()
# load nhiều thể loại
def load_kinds():
    return KindOfRoom.query.all()

# Lấy 1st ảnh theo thể loại
def get_kinds_image():
    kinds  = KindOfRoom.query.all()
    dic = {}
    for k in kinds:
        for x in k.images:
            if x.rank == 1:
               dic[k.id] = x.link
    return dic

def load_countries():
    return [p for p in pycountry.countries]
if __name__ == "__main__":
    print(load_countries())
    pass