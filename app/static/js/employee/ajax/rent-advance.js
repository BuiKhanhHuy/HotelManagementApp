// tim kiem theo CMND
function searchIdCard() {
    searchBookRoom()
}

// tim kiem theo ngay nhan phong
function searchFromCheckInDate() {
    searchBookRoom()
}

// tim kiem theo ngay tra phong
function searchToCheckInDate() {
    searchBookRoom()
}

// tim kiem danh sach phong dat
function searchBookRoom() {
    let identification_card = document.getElementById('filter-id-card')
    let checkFromInDate = document.getElementById('filter-from-check-in-date')
    let checkToInDate = document.getElementById('filter-to-check-in-date')

    let valueIdentification_card = identification_card.value
    let valueFromCheckInDate = checkFromInDate.value
    let valueToCheckInDate = checkToInDate.value

    // api search book room
    apiSearchBookRoom(valueIdentification_card,
        valueToCheckInDate, valueFromCheckInDate)
}

// reset filter
function resetFilter(){
    let identification_card = document.getElementById('filter-id-card')
    let checkFromInDate = document.getElementById('filter-from-check-in-date')
    let checkToInDate = document.getElementById('filter-to-check-in-date')

    identification_card.value = ''
    checkToInDate.value = ''
    checkFromInDate.value = ''

    // api search book room
    apiSearchBookRoom('', '', '')
}

// api search book room
function apiSearchBookRoom(valueIdentification_card, valueFromCheckInDate,
                           valueToCheckInDate) {
    // gui len server
    fetch('/api/employee/rent-advance/find-book-room', {
        method: 'post',
        body: JSON.stringify({
            'identification_card': valueIdentification_card,
            'check_from_in_date': valueFromCheckInDate,
            'check_to_in_date': valueToCheckInDate
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
function getHTMLRoomInBookRoom(bookRoom) {
    let txtRoomNumber = ''
    let txtStatus = ''
    let txtButton = ''

    for (let i = 0; i < bookRoom['room_numbers'].length; i++)
        txtRoomNumber += bookRoom['room_numbers'][i] + ', '

    if (bookRoom['active'] === true && bookRoom['done'] === false) {
        if (bookRoom['days'] > 0) {
            txtStatus = `<span class="badge badge-pill badge-warning">Phiếu đăt phòng đã quá hạn nhận phòng
                          <span class="font-weight-bold text-dark"> ${bookRoom['days']} </span> ngày </span>`
        } else {
            txtStatus = `<span class="badge badge-pill badge-success">Chờ nhận phòng</span>`
        }
        txtButton = `<button value=""
                        class="btn btn-info text-white shadow-none"
                        id=""
                        onclick="">Nhận phòng</button>`
    } else if (bookRoom['active'] === false && bookRoom['done'] === false) {
        txtStatus = `<span class="badge badge-pill badge-danger">Phiếu đặt phòng đã bị hủy do quá hạn</span>`
        txtButton = `<button value=""
                        class="btn btn-danger text-white shadow-none"
                        id=""
                        onclick="">Xóa phiếu</button>`
    }

    return `
    <tr>
        <td class="text-dark col-1 text-center align-middle">
            ${bookRoom['booking_date']}
        </td>
        <td value=""
            class="text-dark col-1 text-center align-middle">
            ${bookRoom['check_in_date']}
        </td>
        <td value=""
            class="text-dark col-1 text-center align-middle">
            ${bookRoom['check_out_date']}
        </td>
        <td value=""
            class="text-dark col-2 align-middle">
             ${bookRoom['customer_name']}
        </td>
        <td value=""
            class="text-danger text-center col-1 font-weight-bold align-middle">
            ${bookRoom['identification_card']}
        </td>
        <td class="text-dark col-2 align-middle">
            ${txtRoomNumber}
        </td>
        <td class="text-dark col-2 align-middle">
            ${txtStatus}
        </td>
        <td class="text-dark col-2 text-center align-middle">
            ${txtButton}
        </td>
    </tr>
    `
}