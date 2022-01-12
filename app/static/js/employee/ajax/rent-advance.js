// tim kiem theo CMND
function searchIdCard() {
    searchBookRoom()
}

// tim kiem theo ngay nhan phong
function searchCheckInDate() {
    searchBookRoom()
}

// tim kiem theo ngay tra phong
function searchCheckOutDate() {
    searchBookRoom()
}

// tim kiem danh sach phong dat
function searchBookRoom() {
    let identification_card = document.getElementById('filter-id-card')
    let checkInDate = document.getElementById('filter-check-in-date')
    let checkOutDate = document.getElementById('filter-check-out-date')

    let valueIdentification_card = identification_card.value
    let valueCheckInDate = checkInDate.value
    let valueCheckOutDate = checkOutDate.value

    // api search book room
    apiSearchBookRoom(valueIdentification_card,
        valueCheckInDate, valueCheckOutDate)
}

// reset filter
function resetFilter() {
    let identification_card = document.getElementById('filter-id-card')
    let checkInDate = document.getElementById('filter-check-in-date')
    let checkInOutDate = document.getElementById('filter-check-out-date')

    identification_card.value = ''
    checkInDate.value = ''
    checkInOutDate.value = ''

    // api search book room
    apiSearchBookRoom('', '', '')
}

// api search book room
function apiSearchBookRoom(valueIdentification_card, valueCheckInDate,
                           valueCheckOutDate) {
    // gui len server
    fetch('/api/employee/rent-advance/find-book-room', {
        method: 'post',
        body: JSON.stringify({
            'identification_card': valueIdentification_card,
            'check_in_date': valueCheckInDate,
            'check_out_date': valueCheckOutDate
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(res => res.json()).then(data => {
        if (data.code === 200) {
            let contentRoom = document.getElementById('content-room')
            let txtContentRoom = ''

            for (let i = 0; i < data['book_room_list'].length; i++)
                txtContentRoom += getHTMLRoomInBookRoom(data['book_room_list'][i])
            contentRoom.innerHTML = txtContentRoom
        }
    }).catch(error => console.log(error))
}


// do HTMl ra giao dien cac phong da dat
// dat o phan HTMl
// function getHTMLRoomInBookRoom(bookRoom) {
//     let txtRoomNumber = ''
//     let txtStatus = ''
//     let txtButton = ''
//
//     for (let i = 0; i < bookRoom['room_numbers'].length; i++)
//         txtRoomNumber += bookRoom['room_numbers'][i] + ', '
//
//     if (bookRoom['active'] === true && bookRoom['done'] === false) {
//         if (bookRoom['days'] > 0) {
//             txtStatus = `<span class="badge badge-pill badge-warning">Phiếu đăt phòng đã quá hạn nhận phòng
//                           <span class="font-weight-bold text-dark"> ${bookRoom['days']} </span> ngày </span>`
//         } else {
//             txtStatus = `<span class="badge badge-pill badge-success">Chờ nhận phòng</span>`
//         }
//         txtButton = `<a href="">
//                          <button class="btn btn-info text-white shadow-none"
//                         onclick="">Nhận phòng</button>
//                         </a>`
//     } else if (bookRoom['active'] === false && bookRoom['done'] === false) {
//         txtStatus = `<span class="adge badge-pill badge-danger">Phiếu đặt phòng đã bị hủy do quá hạn</span>`
//         txtButton = `<button class="btn btn-danger text-white shadow-none"
//                     onclick="inactiveBookRoom(${bookRoom['book_room_id']})">Không hiển thị</button>`
//     }
//     return `
//     <tr id="book-room-${bookRoom['book_room_id']}">
//         <td class="text-dark col-1 text-center align-middle">
//             ${bookRoom['booking_date']}
//         </td>
//         <td class="text-dark col-1 text-center align-middle">
//             ${bookRoom['check_in_date']}
//         </td>
//         <td class="text-dark col-1 text-center align-middle">
//             ${bookRoom['check_out_date']}
//         </td>
//         <td class="text-dark col-2 align-middle">
//              ${bookRoom['customer_name']}
//         </td>
//         <td class="text-danger text-center col-1 font-weight-bold align-middle">
//             ${bookRoom['identification_card']}
//         </td>
//         <td class="text-dark col-2 align-middle">
//             ${txtRoomNumber}
//         </td>
//         <td class="text-dark col-2 align-middle">
//             ${txtStatus}
//         </td>
//         <td class="text-dark col-2 text-center align-middle">
//             ${txtButton}
//         </td>
//     </tr>
//     `
// }


// tat hoat dong cua phieu dat phong het han
function inactiveBookRoom(bookRoomId) {
    let bookRoom = document.getElementById(`book-room-${bookRoomId}`)

    fetch(`/api/employee/rent-advance/inactive-book-room/${bookRoomId}`, {
        method: 'delete'
    }).then(res => res.json()).then(data => {
        if (data.code === 200) {
            // an book room
            bookRoom.style.display = 'none'
        }
    }).catch(error => console.log(error))
}