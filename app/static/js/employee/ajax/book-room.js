// lay html cua phong
function getRoomHTML(room) {
    return `<tr>
                <td class="text-dark col-md-1 text-middle align-middle">
                    <img src="${room['image']}" class="img-fluid" alt="image">
                </td>
                <td class="text-dark col-md-1 text-center align-middle">${room['room_number']}</td>
                <td class="text-dark col-md-1 text-center align-middle">${room['maximum_number']}
                    khách
                </td>
                <td class="text-dark col-md-2 align-middle">${room['kind_of_room_name']}</td>
                <td class="text-danger col-md-2 font-weight-bold align-middle">${room['price'].toLocaleString()}
                    VND
                </td>
                <td class="text-dark col-md-3 align-middle">${room['description']}</td>
                <td class="text-dark col-md-2 text-center align-middle">
                    <button value="${room['id']}" class="btn btn-info text-white btn-choose-book-room btn-choose-room shadow-none" 
                    id="id-btn-choose-room-${room['id']}" 
                    onclick="btnButtonAddBookRoomClick(${room['id']}, '${room['room_number']}', 
                    '${room['kind_of_room_name']}', ${room['price']}, '${room['image']}')">Chọn phòng</button>
                </td>
            </tr>`
}


// click chon them phong dat
function btnButtonAddBookRoomClick(roomId, roomNumber, kindOfRoomName, price, image, room) {
    // hieu ung
    clickButtonChooseRoom(roomId, room)
    // gui du lieu len server
    addToBookRoomCart(roomId, roomNumber, kindOfRoomName, price, image)
}

// them phong vao bo nho dat phong
function addToBookRoomCart(roomId, roomNumber, kindOfRoomName, price, image) {
    fetch('/api/employee/book-room/add-to-book-room-cart', {
        method: 'post',
        body: JSON.stringify({
            'room_id': roomId,
            'room_number': roomNumber,
            'kind_of_room_name': kindOfRoomName,
            'price': price,
            'image': image
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(res => res.json()).then(data => {
        if (data.code === 200) {
            if (data['isAdd'] === true)
                notification(1, `Đã thêm thành công phòng ${roomNumber}.`)
            else
                notification(1, `Đã hủy thành công phòng ${roomNumber}.`)

            let totalBookRoom = document.getElementById('total-book-room')
            if (data['total_room'] != null)
                totalBookRoom.innerText = data['total_room']
            else
                totalBookRoom.innerText = 0
        }
    }).catch(error => error => console.log(error))
}

// refresh session book room
function cleanBookRoomInSession() {
    fetch('/api/employee/book-room/clean-book-room', {
        method: 'delete',
    }).then(res => res.json()).then(data => {
        if (data.code === 200) {
            location.reload()
        }
    }).catch(error => error => console.log(error))
}