from app.models import *


# load rooms
def load_rooms():
    return Room.query.all()