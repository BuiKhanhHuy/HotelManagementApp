// goi y cmnd va dien thong tin khach hang o phan xac nhan dat phong
document.addEventListener('DOMContentLoaded', () => {
    const input = document.querySelector('input.card-book-room');
    const awesomplete = new Awesomplete(input);

    input.addEventListener('keyup', (e) => {
        var code = (e.keyCode || e.which);
        let valueInput = ''
        valueInput = input.value.toString()

        if (code >= 65 && code <= 90 || code >= 97 && code <= 105 || code >= 48 && code <= 57) {
            fetch(`/api/employee/book-room/get-identification_card`, {
                method: 'post',
                body: JSON.stringify({
                    'id_value': valueInput
                }),
                headers: {
                    'Content-Type': 'application/json'
                }
            }).then(res => res.json()).then(data => {
                if (data.code === 200) {
                    // console.log(data['identification_cards'])
                    awesomplete.list = data['identification_cards']
                }
            }).catch(error => console.log(error))
        } else {
            if (code === 13) {
                // khi nguoi dung chon duoc cmnd co san
                loadCustomerFromIdCard(valueInput)
                return 0;
            }
        }
    });
});

// lay thong tin khach hang thong qua cmnd
function loadCustomerFromIdCard(id_card) {
    fetch(`/api/employee/book-room/get-customer`, {
        method: 'post',
        body: JSON.stringify({
            'id_card': id_card
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(res => res.json()).then(data => {
        if (data.code === 200) {
            if (data['customer']) {
                // lay duoc thong tin khach hang tu id_card
                console.log('Load khach hang ra form')
                loadCustomerIntoForm(data['customer'])
            } else {
                // khong tim duoc khach hang do gt = null
                console.log('Lay thông tin khach hang moi, khach hang nhap thong tin.')
                return 0;
            }
        }
    }).catch(error => console.log(error))
}

// load thong tin khach hang len form
function loadCustomerIntoForm(dicCustomer) {

    let nameBookRoom = document.getElementById('name-book-room');

    let maleBookRoom = document.getElementById('male-book-room');
    let femaleBookRoom = document.getElementById('female-book-room');

    // let idCardBookRoom = document.getElementById('id-card-book-room');

    let optionCusType1 = document.getElementById('option-cus-type-1');
    let optionCustype2 = document.getElementById('option-cus-type-2');

    let phoneBookRoom = document.getElementById('phone-book-room');

    let addressBookRoom = document.getElementById('address-book-room');

    // gan du lieu

    // ten
    nameBookRoom.value = `${dicCustomer['name']}`;

    // gioi tinh
    if (dicCustomer['gender'])
    {
        maleBookRoom.checked = true;
        femaleBookRoom.checked = false;
    }
    else
    {
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