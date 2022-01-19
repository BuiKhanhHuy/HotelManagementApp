function add_to_book_room(room_id, room_number,
                          kind_of_room_name, price) {

    fetch('/api/booking/add-to-book-room-cart', {
        method: 'post',
        body: JSON.stringify({
            'room_id': room_id,
            'room_number': room_number,
            'kind_of_room_name': kind_of_room_name,
            'price': price
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(res => res.json()).then(function (data) {
        let counter = document.getElementById('cusCartCounter')
        if (counter != null)
            counter.innerText = data['total_room']

        let buttonRooms = document.getElementById(`room-${room_id}`)
        let buttonRoomDetail = document.getElementById(`room-detail-${room_id}`)

        if (buttonRooms != null)
            buttonRooms.innerHTML = getHTMLButonAddToCartRooms(room_id, room_number, kind_of_room_name, price, data['room_list'])
        if (buttonRoomDetail != null)
            buttonRoomDetail.innerHTML = getHTMLButtonAddToCartRoomDetail(room_id, room_number, kind_of_room_name, price, data['room_list'])
    }).catch(function (err) {
        alert("Lỗi:" + err)
    })

}

// html button dat phong ngoai phong
function getHTMLButonAddToCartRooms(roomId, roomNumber,
                                    kindOfRoomName, price, roomList) {
    let txtButton = ''
    if (roomList != null) {
        if (roomId.toString() in roomList) {
            txtButton = `<button class="btn btn-secondary btn-block text-center w-75 text-white mx-auto"
                    onclick="add_to_book_room(${roomId},'${roomNumber}','${kindOfRoomName}', ${price})">
                Hủy chọn
            </button>`;
        } else {
            txtButton = `<button class="btn btn-warning btn-block text-center w-75 text-white mx-auto"
                   onclick="add_to_book_room(${roomId},'${roomNumber}','${kindOfRoomName}', ${price})">
                Thêm vào giỏ hàng
            </button>`;
        }
    } else {
        txtButton = `<button class="btn btn-warning btn-block text-center w-75 text-white mx-auto"
                onclick="add_to_book_room(${roomId},'${roomNumber}','${kindOfRoomName}', ${price})">
            Thêm vào giỏ hàng
        </button>`;
    }
    return txtButton;
}

// html dat phong o chi tiet dat phong
function getHTMLButtonAddToCartRoomDetail(roomId, roomNumber,
                                          kindOfRoomName, price, roomList) {
    let txtButton = ''
    if (roomList != null) {
        if (roomId.toString() in roomList) {
            txtButton = `<div class="button-add bg-secondary"
                             onclick="add_to_book_room(${roomId},'${roomNumber}','${kindOfRoomName}', ${price})">
                            <a class="text-white" href="javascript: void(0)"><i class=" fas fa-cart-plus"></i> Hủy khỏi giỏ hàng</a>
                        </div>`;
        } else {
            txtButton = `<div class="button-add"
                             onclick="add_to_book_room(${roomId},'${roomNumber}','${kindOfRoomName}', ${price})">
                            <a href="javascript: void(0)"><i class=" fas fa-cart-plus"></i> Thêm vào giỏ hàng</a>
                        </div>`;
        }
    } else {
        txtButton = `<div class="button-add"
                             onclick="add_to_book_room(${roomId},'${roomNumber}','${kindOfRoomName}', ${price})">
                            <a href="javascript: void(0)"><i class=" fas fa-cart-plus"></i> Thêm vào giỏ hàng</a>
                    </div>`;
    }
    return txtButton;
}


function cal_day(d1, d2) {
    var t2 = d2.getTime();
    var t1 = d1.getTime();

    return Math.floor((t2 - t1) / (24 * 3600 * 1000));
}

function del_cus_cart_booking(room_id) {
    if (confirm("Bạn có chắc chắn xóa phòng này khỏi giỏ hàng không?") === true) {
        fetch('/api/delete-cart-booking/' + room_id, {
            method: 'delete',
            headers: {
                'Content-Type': 'application/json'
            }
        }).then(function (res) {
            console.info(res)
            return res.json()
        }).then(function (data) {
            let counter = document.getElementById('cusCartCounter')
            let counter2 = document.getElementById('total')
            counter.innerText = data.total_room
            counter2.innerText = data.total_room

            if (data.total_room > 0) {
                document.getElementById('order').style.display = ''
            } else {
                document.getElementById('order').style.display = 'none'
            }

            let e = document.getElementById("room" + room_id)
            e.style.display = "none"
        }).catch(function (err) {
            console.log("Lỗi:" + err)
        })
    }
}