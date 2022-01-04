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
                    <button value="1" class="btn btn-info text-white btn-choose-book-room shadow-none" 
                    onclick="btnButtonAddBookRoomClick(this, ${room['id']}, '${room['room_number']}', 
                    '${room['kind_of_room_name']}', ${room['price']}, '${room['image']}')">Chọn phòng</button>
                </td>
            </tr>`
}

// click chon them phong dat
function btnButtonAddBookRoomClick(objButton, roomId, roomNumber, kindOfRoomName, price, image) {
    // // hieu ung
    // customButtonAddBookRoom(objButton)
    // // gui du lieu len server
    // addToBookRoomCart(roomId, roomNumber, kindOfRoomName, price, image)
    alert('hihi')
}

// hieu ung button them vao dat phong duoc click
function customButtonAddBookRoom(objButton) {
    if (parseInt(objButton.value) === 1) {
        objButton.value = 0
        objButton.innerText = "Hủy chọn";
        objButton.setAttribute("style", "background-color: #8f8a8a; border-color: #8f8a8a;");
    } else {
        objButton.value = 1
        objButton.innerText = "Chọn phòng";
        objButton.setAttribute("style", "background-color: #2cabe3; border-color: #2cabe3;");
    }
}

// them phong vao bo nho dat phong
function addToBookRoomCart(roomId, roomNumber, kindOfRoomName, price, image) {
    fetch('/employee/add-to-book-room-cart', {
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
            alert(`Đã thêm thành công ${data['total_room']} phong`)
        }
    }).catch(error => {

    })
}

