// thiết lập thời gian cố định
function setUpDateTime(){
    var check_in = document.getElementById("checkin_date")
    var check_out = document.getElementById("checkout_date")
    let current_day = new Date(Date.now());
    // Ngay check in la ngay mai
    current_day.setUTCHours(14, 0, 0, 0)
    current_day.setDate(current_day.getDate() + 1);
    check_in.value = current_day.toISOString().substring(0, 10);
    // Ngay check out la sau ngay mai
    current_day.setUTCHours(12, 0, 0, 0)
    current_day.setDate(current_day.getDate() + 1);
    check_out.value = current_day.toISOString().substring(0, 10);
}
//thiết lập ngày, không được nhận phòng trước ngày đặt
function checkDate(startDate, endDate) {
    return startDate < endDate;
}
