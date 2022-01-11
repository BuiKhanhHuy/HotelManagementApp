// api them khach hang vao session thue phong truc tiep
function addCustomerToRent(name, gender, customerTypeId, identificationCard,
                           phoneNumber, address, room_id, numberOfChoose) {
    fetch('/api/employee/rent-directly/add-customer', {
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
            let roomId = data['room_id']
            let contentCustomerInRoom = document.getElementById(`content-customer-${roomId}`)
            let contentText = ''

            // do du lieu khach hang ra HTML
            for(let customer in data['customers'])
            {
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

    if(customer.customer_type_id === 1)
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