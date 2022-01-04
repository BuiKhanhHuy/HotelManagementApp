// lay html cua phong
function getRoomHTML(room) {
    return `<tr>
                <td class="text-dark col-md-1 text-middle align-middle">
                    <img src="${room['image']}" class="img-fluid" alt="image">
                </td>
                <td class="text-dark col-md-1 text-center align-middle">${room['room_number']}</td>
                <td class="text-dark col-md-1 text-center align-middle">${room['maximum_number']}
                    khách
                </td>
                <td class="text-dark col-md-2 align-middle">${room['kind_of_room_name']}</td>
                <td class="text-danger col-md-2 font-weight-bold align-middle">${room['price'].toLocaleString()}
                    VND
                </td>
                <td class="text-dark col-md-3 align-middle">${room['description']}</td>
                <td class="text-dark col-md-2 text-right align-middle">
                    <button value="1" class="btn btn-info text-white btn-choose-rent-directly shadow-none"
                    onclick="btnButtonAddRentRoomClick(this)">Chọn phòng</button>
                </td>
            </tr>`
}

// click chon them phong thue
function btnButtonAddRentRoomClick(objButton){
    alert('oke thue phong')
}

// hieu ung button them vao thue phong duoc click
function customButtonAddRentRoom(){

}

// them phong vao bo nho thue phong
function addToRentRoomCart(){

}
