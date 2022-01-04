const btnBookRoom = document.getElementsByClassName('btn-choose-book-room');

for (let i = 0; i < btnBookRoom.length; i++) {
    btnBookRoom[i].onclick = function () {
        // hàm thực hiện
        alert('book room')
    }
}

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
                    <button class="btn btn-dark text-white btn-choose-book-room 
                                    btn-choose-rent-directly">Chọn phòng</button>
                </td>
            </tr>`
}
