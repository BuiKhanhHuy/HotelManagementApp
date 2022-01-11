// load thong tin khach hang len form
function loadCustomerIntoForm(dicCustomer) {
    let name = document.getElementById('name')
    let gender = document.getElementById('gender')
    let phoneNumber = document.getElementById('phone-number')
    let address = document.getElementById('address')
    let customerTypeId = document.getElementById('customer-type-id')

    // gan du lieu
    name.value = dicCustomer['name']
    gender.value = dicCustomer['gender'] === true ? 1 : 0
    customerTypeId.value = dicCustomer['customer_type_id']
    phoneNumber.value = dicCustomer['phone_number']
    address.value = dicCustomer['address']
}


// kiem tra nhap lieu day du thong tin
function checkInputCustomer(valueName, valueGender, valueCustomerTypeId, valueIdentificationCard,
                            valuePhoneNumber, valueAddress, valueRoomId) {
    let flag = false

    if (valueName === '') {
        flag = true;
    } else if (valueGender === '') {
        flag = true;
    } else if (valueCustomerTypeId === '') {
        flag = true;
    } else if (valueIdentificationCard === '') {
        flag = true;
    } else if (valuePhoneNumber === '') {
        flag = true;
    } else if (valueAddress === '') {
        flag = true;
    } else if (isNaN(valueRoomId)) {
        flag = true;
    }
    return flag;
}

// kiem tra khach hang da co  trong danh sach dua vao cmnd
function CheckExistingCustomerInList(idCard, objICardList) {
    for (let i = 0; i < objICardList.length; i++)
        if (idCard === objICardList[i].innerText.split(' ').join(''))
            return true
    return false
}

// reset form
function resetForm(name, gender, customerTypeId, identificationCard,
                   phoneNumber, address, roomId) {
    name.value = ''
    gender.value = 1
    customerTypeId.value = 1
    identificationCard.value = ''
    phoneNumber.value = ''
    address.value = ''
    roomId.value = ''
}


// them khach hang vao session thue phong
function clickAddCustomer() {
    // lay phan tu
    let name = document.getElementById('name')
    let identificationCard = document.getElementById('identification-card')
    let gender = document.getElementById('gender')
    let phoneNumber = document.getElementById('phone-number')
    let address = document.getElementById('address')
    let customerTypeId = document.getElementById('customer-type-id')
    let roomId = document.getElementById('room-id')

    let idCardList = document.getElementsByClassName('id-card')

    // lay gia tri
    let valueName = name.value
    let valueIdentificationCard = identificationCard.value.split(' ').join('')
    let valueGender = gender.value
    let valuePhoneNumber = phoneNumber.value
    let valueAddress = address.value
    let valueCustomerTypeId = parseInt(customerTypeId.value)
    let valueRoomId = parseInt(roomId.value)

    // kiem tra khach hang da co trong danh sach
    if (CheckExistingCustomerInList(valueIdentificationCard, idCardList)) {
        // hien thi loi
        let txtTile = 'Lỗi'
        let txtBody = 'Khách hàng đã được phân phòng.'
        showModal(txtTile, txtBody)
        // reset form
        resetForm(name, gender, customerTypeId, identificationCard,
            phoneNumber, address, roomId)
        return;
    }

    // kiem tra gia tri input
    if (checkInputCustomer(valueName, valueGender, valueCustomerTypeId, valueIdentificationCard,
        valuePhoneNumber, valueAddress, valueRoomId)) {
        return;
    }

    // so phong nguoi toi da cua mot phong
    let numberOfChoose = document.getElementById(`room-id-${valueRoomId}`)
    let valueNumberOfChoose = parseInt(numberOfChoose.getAttribute('data-number-choose'))

    // neu phong do chua du so nguoi toi da thi van cho phep them vao phong
    if (valueNumberOfChoose > 0) {
        // tru di so nguoi toi da
        valueNumberOfChoose -= 1
        numberOfChoose.setAttribute('data-number-choose', valueNumberOfChoose.toString())

        // them khach hang bang api
        addCustomerToRent(valueName, valueGender, valueCustomerTypeId,
            valueIdentificationCard, valuePhoneNumber, valueAddress, valueRoomId,
            valueNumberOfChoose)

        // reset form
        resetForm(name, gender, customerTypeId, identificationCard, phoneNumber, address, roomId)

    } else {
        // het cho thi bao loi
        let txtError = 'Phòng này đã đủ số người tối đa!'
        showModal('Lỗi !', txtError)
    }
}
