// load thong tin khach hang len form
function loadCustomerIntoForm(dicCustomer) {

    let nameBookRoom = document.getElementById('name-book-room');

    let maleBookRoom = document.getElementById('male-book-room');
    let femaleBookRoom = document.getElementById('female-book-room');


    let optionCusType1 = document.getElementById('option-cus-type-1');
    let optionCustype2 = document.getElementById('option-cus-type-2');

    let phoneBookRoom = document.getElementById('phone-book-room');

    let addressBookRoom = document.getElementById('address-book-room');

    // gan du lieu

    // ten
    nameBookRoom.value = `${dicCustomer['name']}`;

    // gioi tinh
    if (dicCustomer['gender']) {
        maleBookRoom.checked = true;
        femaleBookRoom.checked = false;
    } else {
        femaleBookRoom.checked = true;
        maleBookRoom.checked = false;
    }


    // CMND da co

    // loai khach hang
    if (dicCustomer['customer_type_id'] === 1) {
        // khach trong nuoc
        optionCusType1.selected = true
    } else {
        // khach nuoc ngoai
        optionCustype2.selected = true
    }

    // so dien thoai
    phoneBookRoom.value = dicCustomer['phone_number']

    // dia chi
    addressBookRoom.value = dicCustomer['address']
}

// xoa phong trong danh sach dat phong chi tiet
function deleteRoomInBookRoomDetail(roomId) {
    fetch(`/api/employee/book-room/delete-room/${roomId}`, {
        method: 'delete',
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(res => res.json()).then(data => {
        let room;
        if (data.code === 200) {
            room = document.getElementById(`tr-room-${roomId}`)
            room.style.display = 'none'
            if (data['total_room'] === 1) {
                disabledDelRoomButton()
            }

            notification(1, `Xóa thành công.`)

            let txtRoomNumbers = ''
            let roomNumbers = document.getElementById('room_number')
            for (let i = 0; i < data['room_numbers'].length; i++)
                txtRoomNumbers += `${data['room_numbers'][i]}, `
            roomNumbers.innerText = txtRoomNumbers
        }
    }).catch(error => console.log(error))
}

// disabled button xoa phong
function disabledDelRoomButton() {
    let btnDelRoom = document.getElementsByClassName('btn-del-room')
    for (let i = 0; i < btnDelRoom.length; i++)
        btnDelRoom[i].disabled = true;
}