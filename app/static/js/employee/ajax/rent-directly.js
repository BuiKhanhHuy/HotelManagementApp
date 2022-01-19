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
                <td class="text-dark col-md-2 text-right align-middle">
                      <button value="${room['id']}" class="btn btn-info text-white btn-choose-rent-room btn-choose-room shadow-none"
                    id="id-btn-choose-room-${room['id']}"
                    onclick="btnButtonAddRentRoomClick(${room['id']}, '${room['room_number']}',
                    '${room['kind_of_room_name']}', ${room['price']}, '${room['image']}', ${room['maximum_number']})">
                    Chọn phòng</button>
                </td>
            </tr>`
}

// click chon them phong dat
function btnButtonAddRentRoomClick(roomId, roomNumber, kindOfRoomName, price, image, maximum_number) {
    // hieu ung
    clickButtonChooseRoom(roomId)
    // gui du lieu len server
    addToRentRoomCart(roomId, roomNumber, kindOfRoomName, price, image, maximum_number)
}

// them phong vao bo nho thue phong
function addToRentRoomCart(roomId, roomNumber, kindOfRoomName, price, image, maximum_number) {
    fetch('/api/employee/rent-directly/add-to-rent-directly-cart', {
        method: 'post',
        body: JSON.stringify({
            'room_id': roomId,
            'room_number': roomNumber,
            'kind_of_room_name': kindOfRoomName,
            'price': price,
            'image': image,
            'maximum_number': maximum_number
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
                totalBookRoom.innerText = '0'
        }
    }).catch(error => error => console.log(error))
}