// thiết lập thời gian cố định
var check_in = document.getElementById("check-in-date")
var check_out = document.getElementById("check-out-date")
let current_day = new Date(Date.now());

current_day.setHours(14, 0, 0, 0)
current_day.setDate(current_day.getDate() + 1);

check_in.min = current_day.toISOString().substring(0, 10)
check_out.min = current_day.toISOString().substring(0, 10)

// Ngay check in la ngay mai
if (check_in.value === '') {
    check_in.value = current_day.toISOString().substring(0, 10)
}
// Ngay check out la sau ngay mai
if (check_out.value === '') {
    current_day.setHours(12, 0, 0, 0)
    current_day.setDate(current_day.getDate() + 1);
    check_out.value = current_day.toISOString().substring(0, 10);
}

// kiem tra gia tri check-in check-out da nhap chua
function checkCheckInOut() {
    let checkInDate = document.getElementById('check-in-date')
    let checkOutDate = document.getElementById('check-out-date')

    return !(checkInDate.value === '' || checkOutDate.value === '');
}

// kiem tra ngay chon co hop le
function checkDate(startDate, endDate) {
    return startDate <= endDate;
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

    if (checkOutDate.value !== '') {
        if (!checkDate(valueCheckInDate, valueCheckOutDate)) {
            printError('Ngày nhận phòng phải nhỏ hơn ngày trả phòng !')
            checkInDate.value = ''
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


    if (checkInDate.value === '') {
        printError('Bạn vui lòng chọn ngày nhận phòng !')
        checkOutDate.value = ''
    } else if (!checkDate(valueCheckInDate, valueCheckOutDate)) {
        printError('Ngày trả phòng phải lớn hơn ngày nhận phòng !')
        checkOutDate.value = ''
    }
}

// print error
function printError(err) {
    let error = document.getElementById('error')

    error.innerText = err
    setTimeout(function () {
        error.innerText = ''
    }, 1500);
}