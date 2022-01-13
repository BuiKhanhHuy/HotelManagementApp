// tim kiem theo so phong
function searchRoomNumber() {
    searchRentRoom()
}

// tim kiem theo ngay nhan phong
function searchCheckInDate() {
    searchRentRoom()
}

// tim kiem theo ngay tra phong
function searchCheckOutDate() {
    searchRentRoom()
}

// tim kiem danh sach phong dat
function searchRentRoom() {
    let roomNumber = document.getElementById('filter-room-number')
    let checkInDate = document.getElementById('filter-check-in-date')
    let checkOutDate = document.getElementById('filter-check-out-date')

    let valueRoomNumber = roomNumber.value
    let valueCheckInDate = checkInDate.value
    let valueCheckOutDate = checkOutDate.value
    // api search book room
    apiSearchRentRoom(valueRoomNumber, valueCheckInDate, valueCheckOutDate)
}

// reset filter
function resetFilter() {
    let roomNumber = document.getElementById('filter-room-number')
    let checkInDate = document.getElementById('filter-check-in-date')
    let checkInOutDate = document.getElementById('filter-check-out-date')

    roomNumber.value = ''
    checkInDate.value = ''
    checkInOutDate.value = ''

    apiSearchRentRoom('', '', '')
}

// api search book room
function apiSearchRentRoom(roomNumber, checkInDate, checkOutDate) {
    // gui len server
    fetch('/api/employee/payment/find-rent', {
        method: 'post',
        body: JSON.stringify({
            'room_number': roomNumber,
            'check_in_date': checkInDate,
            'check_out_date': checkOutDate
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(res => res.json()).then(data => {
        if (data.code === 200) {
            let contentRoom = document.getElementById('content-rent')
            let txtContentRoom = ''

            for (let i = 0; i < data['rent_list'].length; i++)
                txtContentRoom += getHTMLRentRoom(data['rent_list'][i])
            contentRoom.innerHTML = txtContentRoom
        }
    }).catch(error => console.log(error))
}



