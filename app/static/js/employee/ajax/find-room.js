// =======BUTTON LUC DAT PHONG VA THUE PHONG TRUC TIEP========
// tham so hieu ung click
const dicValueButton = {};
let btnChooseRoom = document.getElementsByClassName('btn-choose-room')
for (let i = 0; i < btnChooseRoom.length; i++) {
    dicValueButton[btnChooseRoom[i].value] = 0
}

// hieu ung button them vao dat phong duoc click
function clickButtonChooseRoom(roomId) {
    if (dicValueButton[roomId] === 0) {
        dicValueButton[roomId] = 1
    } else {
        dicValueButton[roomId] = 0
    }
    customButtonChooseRoom(roomId, dicValueButton)
}

// thay doi hieu ung nut
function customButtonChooseRoom(roomId, dicValueButton) {
    let btnChooseRoom = document.getElementById(`id-btn-choose-room-${roomId}`)
    console.log(dicValueButton)
    if (dicValueButton[roomId] === 1) {
        btnChooseRoom.innerText = "Hủy chọn";
        btnChooseRoom.setAttribute("style", "background-color: #8f8a8a; border-color: #8f8a8a;");
    } else {
        btnChooseRoom.innerText = "Chọn phòng";
        btnChooseRoom.setAttribute("style", "background-color: #2cabe3; border-color: #2cabe3;");
    }

}



// ===========LOC THONG TIN PHONG CAN DAT, CAN THUE===========
// kiem tra ngay chon co hop le
function checkDate(startDate, endDate) {
    return startDate <= endDate;
}

// kiem tra gia tri check-in check-out da nhap chua
function checkCheckInOut() {
    let checkInDate = document.getElementById('check-in-date')
    let checkOutDate = document.getElementById('check-out-date')

    return !(checkInDate.value === '' || checkOutDate.value === '');
}

// bat su kien onchange cua check-in
function checkCheckInDate(type) {
    let checkInDate = document.getElementById('check-in-date')
    let valueCheckInDate = new Date(checkInDate.value)
    valueCheckInDate.setHours(14, 0, 0)

    let checkOutDate = document.getElementById('check-out-date')
    let valueCheckOutDate = new Date(checkOutDate.value)
    valueCheckOutDate.setHours(12, 0, 0, 0)

    let today = new Date(Date.now())
    // today.setHours(14, 0, 0)
    // neu la thue phong truc tiep thì tinh nguyen ngay hom nay
    if (type === 2) {
        today = new Date(Date.now())
        today.setHours(13, 0, 0)
    }

    let txtTitle = 'Lỗi !'
    let txtBody = ''

    if (!checkDate(today, valueCheckInDate)) {
        disableButtonChooseRoom(true)
        txtBody = 'Ngày nhận phòng phải lớn hơn ngày hôm nay !'
        showModal(txtTitle, txtBody)
        checkInDate.value = ''
    } else if (checkOutDate.value !== '') {
        if (!checkDate(valueCheckInDate, valueCheckOutDate)) {
            disableButtonChooseRoom(true)
            txtBody = 'Ngày nhận phòng phải nhỏ hơn ngày trả phòng !'
            showModal(txtTitle, txtBody)
            checkInDate.value = ''
        } else {
            disableButtonChooseRoom(false)
            findRoom()
        }
    }

}

// bat su kien onchange cua check-out
function checkCheckOutDate() {
    let checkInDate = document.getElementById('check-in-date')
    let checkOutDate = document.getElementById('check-out-date')

    let valueCheckInDate = new Date(checkInDate.value)
    valueCheckInDate.setHours(14, 0, 0, 0)
    let valueCheckOutDate = new Date(checkOutDate.value)
    valueCheckOutDate.setHours(12, 0, 0, 0)

    let txtTitle = 'Lỗi !'
    let txtBody = ''

    if (checkInDate.value === '') {
        disableButtonChooseRoom(true)
        txtBody = 'Bạn vui lòng chọn ngày nhận phòng !'
        showModal(txtTitle, txtBody)
        checkOutDate.value = ''
    } else if (!checkDate(valueCheckInDate, valueCheckOutDate)) {
        disableButtonChooseRoom(true)
        txtBody = 'Ngày trả phòng phải lớn hơn ngày nhận phòng !'
        showModal(txtTitle, txtBody)
        checkOutDate.value = ''
    } else {
        disableButtonChooseRoom(false)
        findRoom()
    }
}

// tim kiem theo so phong
function searchRoomNumber(objRoomNumber) {
    let txtTitle = 'Lỗi !'
    let txtBody = ''
    if (!checkCheckInOut()) {
        disableButtonChooseRoom(true)
        txtBody = 'Bạn vui lòng chọn đầy đủ ngày nhận phòng và ngày trả phòng !'
        showModal(txtTitle, txtBody)
        objRoomNumber.value = ''
    } else {
        disableButtonChooseRoom(false)
        // tim kiem phong
        findRoom()
    }
}

// tim kiem theo bo loc
filters = document.getElementsByClassName('filter-room')
for (let i = 0; i < filters.length; i++) {
    filters[i].onchange = function () {
        if (!checkCheckInOut()) {
            disableButtonChooseRoom(true)
            let txtTitle = 'Lỗi !'
            let txtBody = 'Bạn vui lòng chọn đầy đủ ngày nhận phòng và ngày trả phòng !'
            showModal(txtTitle, txtBody)
        } else {
            disableButtonChooseRoom(false)
            // tim kiem phong
            findRoom()
        }
    }
}

// ham tim phong
function findRoom(page) {
    let filterCheckInDate = document.getElementById('check-in-date')
    let filterCheckOutDate = document.getElementById('check-out-date')
    let filterKindOfRoom = document.getElementById('filter-kind-of-room')
    let filterPrice = document.getElementById('filter-price')
    let filterMaxPeople = document.getElementById('filter-max-people')
    let filterRoomNumber = document.getElementById('filter-room-number')

    let checkInDate = new Date(filterCheckInDate.value)
    checkInDate.setUTCHours(14, 0, 0, 0)
    checkInDate = checkInDate.toJSON()

    let checkOutDate = new Date(filterCheckOutDate.value)
    checkOutDate.setUTCHours(12, 0, 0, 0)
    checkOutDate = checkOutDate.toJSON()

    let idKindOfRoom = parseInt(filterKindOfRoom.value)
    let price = parseFloat(filterPrice.value)
    let maxPeople = parseInt(filterMaxPeople.value)
    let roomNumber = filterRoomNumber.value

    loadRoom(checkInDate, checkOutDate, idKindOfRoom, price, maxPeople, roomNumber, page)
}

// ham load phong
function loadRoom(checkInDate, checkOutDate, idKindOfRoom, price, maxPeople, roomNumber, page = 1) {
    fetch('/api/employee/find-room', {
        method: 'post',
        body: JSON.stringify({
            'check_in_date': checkInDate,
            'check_out_date': checkOutDate,
            'id_kind_of_room': idKindOfRoom,
            'price': price,
            'max_people': maxPeople,
            'room_number': roomNumber,
            'page': page
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(res => res.json()).then(data => {
        if (data.code === 200) {
            let room = document.getElementById('content-room')
            let content = ``

            let length = data['rooms'].length

            for (let i = 0; i < length; i++)
                content += getRoomHTML(data['rooms'][i])
            room.innerHTML = content

            getHTMLPagination(data['iter_pages'])

            for (let i = 0; i < length; i++)
                customButtonChooseRoom(data['rooms'][i]['id'], dicValueButton)
        }
    }).catch(error => console.log(error))
}

// disable button chon phong khi chua nhap ngay checkin, checkout hop le
function disableButtonChooseRoom(flag) {
    let btnChooseRoom = document.getElementsByClassName('btn-choose-room')

    for (let i = 0; i < btnChooseRoom.length; i++) {
        // flag == true -> disable
        btnChooseRoom[i].disabled = !!flag;
    }
}

// lay html pagination
function getHTMLPagination(iter_pages) {
    let iterPages = document.getElementById('pagination')
    let lis = ''

    for (let i = 0; i < iter_pages.length; i++) {
        if (iter_pages[i] == null)
            lis += `<li class="page-item"><a class="page-link"  href="javascript: void(0)">...</a></li>`
        else
            lis += `<li class="page-item"><a class="page-link"  href="javascript: void(0)" onclick="findRoom(${iter_pages[i]})">${iter_pages[i]}</a></li>`
    }
    iterPages.innerHTML = lis
}

