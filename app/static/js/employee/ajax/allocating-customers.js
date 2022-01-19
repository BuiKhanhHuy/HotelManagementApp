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
        notification(2, 'Tên khách hàng là bắt buộc.')
        flag = true;
    } else if (valueGender === '') {
        notification(2, 'Giới tính khách hàng là bắt buộc.')
        flag = true;
    } else if (valueCustomerTypeId === '') {
        notification(2, 'Loại khách hàng là bắt buộc.')
        flag = true;
    } else if (valueIdentificationCard === '') {
        notification(2, 'CMND khách hàng là bắt buộc.')
        flag = true;
    } else if (valuePhoneNumber === '') {
        notification(2, 'Số điện thoại khách hàng là bắt buộc.')
        flag = true;
    } else if (valueAddress === '') {
        notification(2, 'Địa chỉ khách hàng là bắt buộc.')
        flag = true;
    } else if (isNaN(valueRoomId)) {
        notification(2, 'Chọn phòng là bắt buộc.')
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
function clickAddCustomer(addCustomerNumber) {
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
        addCustomerToRent(addCustomerNumber, valueName, valueGender, valueCustomerTypeId,
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

// api them khach hang vao session thue phong truc tiep
function addCustomerToRent(addCustomerNumber, name, gender, customerTypeId, identificationCard,
                           phoneNumber, address, room_id, numberOfChoose) {
    fetch(`/api/employee/add-customer/${addCustomerNumber}`, {
        method: 'post',
        body: JSON.stringify({
            'name': name,
            'gender': gender,
            'customer_type_id': customerTypeId,
            'identification_card': identificationCard,
            'phone_number': phoneNumber,
            'address': address,
            'room_id': room_id,
            'number_of_choose': numberOfChoose
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(res => res.json()).then(data => {
        if (data.code === 200) {
            notification(1, 'Đã thêm khách hàng thành công.')

            let roomId = data['room_id']
            let contentCustomerInRoom = document.getElementById(`content-customer-${roomId}`)
            let contentText = ''

            // do du lieu khach hang ra HTML
            for (let customer in data['customers']) {
                contentText += getHtmlCustomerOnTable(data['customers'][customer])
            }
            contentCustomerInRoom.innerHTML = contentText

            console.log('Thành công')
        } else if (data.code === 500) {
            alert('Server đã có lỗi!')
        }
    }).catch(error => console.log(error))
}

// do html khach hang len table
function getHtmlCustomerOnTable(customer) {
    let txtGender = ''
    let txtCustomerType = ''

    if (customer.gender === 1)
        txtGender = 'Nam'
    else
        txtGender = 'Nữ'

    if (customer.customer_type_id === 1)
        txtCustomerType = 'Nội địa'
    else
        txtCustomerType = 'Nước ngoài'

    return `
            <div class="d-flex ">
                <div class="p-2 border border-1 col-1 text-center">
                    ${customer.customer_id}
                </div>
                <div class="p-2 border border-1 col-2">
                    ${customer.name}
                </div>
                <div class="p-2 border border-1 col-1">
                    ${txtGender}
                </div>
                <div class="p-2 border border-1 col-1">
                    ${txtCustomerType}
                </div>
                <div class="p-2 border border-1 col-2 id-card">
                    ${customer.identification_card}
                </div>
                <div class="p-2 border border-1 col-1">
                    ${customer.phone_number}
                </div>
                <div class="p-2 border border-1 col-4">
                    ${customer.address}
                </div>
            </div>
    `
}