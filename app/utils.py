from app import dao


# all price options
def all_price_options():
    max_price = dao.max_price_of_room()[0]
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


def total_room_in_book_room(book_room_list):
    if book_room_list and 'rooms' in book_room_list:
        return len(book_room_list.get('rooms').keys())
    return 0


if __name__ == '__main__':
    dic = {'a': {'c': 1}}
    print(dic.get('a').get('b'))
