// kiem tra ngay chon co hop le
function checkDate(startDate, endDate) {
    return startDate < endDate;
}

// kiem tra gia tri check-in check-out da nhap chua
function checkCheckInOut() {
    let checkInDate = document.getElementById('check-in-date')
    let checkOutDate = document.getElementById('check-out-date')

    return !(checkInDate.value === '' || checkOutDate.value === '');
}

// bat su kien onchange cua check-in
function checkCheckInDate() {
    let checkInDate = document.getElementById('check-in-date')
    let valueCheckInDate = new Date(checkInDate.value)
    valueCheckInDate.setHours(14, 0, 0)

    let checkOutDate = document.getElementById('check-out-date')
    let valueCheckOutDate = new Date(checkOutDate.value)
    valueCheckOutDate.setHours(12, 0, 0, 0)

    let today = new Date(Date.now())
    today.setHours(14, 0, 0)

    let txtTitle = 'Lỗi !'
    let txtBody = ''

    if (!checkDate(today, valueCheckInDate)) {
        txtBody = 'Ngày nhận phòng phải lớn hơn ngày hôm nay !'
        showBookRoomModal(txtTitle, txtBody)
        checkInDate.value = ''
    } else if (checkOutDate.value !== '' && !checkDate(valueCheckInDate, valueCheckOutDate)) {
        txtBody = 'Ngày nhận phòng phải nhỏ hơn ngày trả phòng !'
        showBookRoomModal(txtTitle, txtBody)
        checkInDate.value = ''
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
        txtBody = 'Bạn vui lòng chọn ngày nhận phòng !'
        showBookRoomModal(txtTitle, txtBody)
        checkOutDate.value = ''
    } else if (!checkDate(valueCheckInDate, valueCheckOutDate)) {
        txtBody = 'Ngày trả phòng phải lớn hơn ngày nhận phòng !'
        showBookRoomModal(txtTitle, txtBody)
        checkOutDate.value = ''
    } else {
        findRoom()
    }
}

// tim kiem theo so phong
function searchRoomNumber(objRoomNumber) {
    let txtTitle = 'Lỗi !'
    let txtBody = ''
    if (!checkCheckInOut()) {
        txtBody = 'Bạn vui lòng chọn đầy đủ ngày nhận phòng và ngày trả phòng !'
        showBookRoomModal(txtTitle, txtBody)
        objRoomNumber.value = ''
    } else {
        // tim kiem phong
        findRoom()
    }
}

// tim kiem theo bo loc
filters = document.getElementsByClassName('filter-room')
for (let i = 0; i < filters.length; i++) {
    filters[i].onchange = function () {
        if (!checkCheckInOut()) {
            let txtTitle = 'Lỗi !'
            let txtBody = 'Bạn vui lòng chọn đầy đủ ngày nhận phòng và ngày trả phòng !'
            showBookRoomModal(txtTitle, txtBody)
        } else {
            // tim kiem phong
            findRoom()
        }
    }
}

// ham tim phong
function findRoom() {
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

    loadRoom(checkInDate, checkOutDate, idKindOfRoom, price, maxPeople, roomNumber)
}

// ham load phong
function loadRoom(checkInDate, checkOutDate, idKindOfRoom, price, maxPeople, roomNumber) {
    fetch('/employee/find-room', {
        method: 'post',
        body: JSON.stringify({
            'check_in_date': checkInDate,
            'check_out_date': checkOutDate,
            'id_kind_of_room': idKindOfRoom,
            'price': price,
            'max_people': maxPeople,
            'room_number': roomNumber
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(res => res.json()).then(data => {
        if (data.code === 200) {
            let room = document.getElementById('content-room')
            let content = ``

            for (let i = 0; i < data['rooms'].length; i++)
                content += getRoomHTML(data['rooms'][i])
            room.innerHTML = content
        }
    }).catch(error => {
        console.log(error)
    })
}

//
// // lay html cua phong
// function getRoomHTML(room) {
//     return `<tr>
//                 <td class="text-dark col-md-1 text-middle align-middle">
//                     <img src="${room['image']}" class="img-fluid" alt="image">
//                 </td>
//                 <td class="text-dark col-md-1 text-center align-middle">${room['room_number']}</td>
//                 <td class="text-dark col-md-1 text-center align-middle">${room['maximum_number']}
//                     khách
//                 </td>
//                 <td class="text-dark col-md-2 align-middle">${room['kind_of_room_name']}</td>
//                 <td class="text-danger col-md-2 font-weight-bold align-middle">${room['price'].toLocaleString()}
//                     VND
//                 </td>
//                 <td class="text-dark col-md-3 align-middle">${room['description']}</td>
//                 <td class="text-dark col-md-2 text-right align-middle">
//                     <button class="btn btn-dark text-white btn-choose-book-room
//                                     btn-choose-rent-directly">Chọn phòng</button>
//                 </td>
//             </tr>`
// }

// show book room modal
function showBookRoomModal(textTitle, textBody) {
    document.getElementById('id-modal-title').innerText = textTitle
    document.getElementById('id-modal-body').innerText = textBody
    $("#bookRoomModal").modal({show: true});
}
