// xoa phong trong danh sach thue phong truc tiep
function deleteRoomInRentDirectly(roomId) {
    fetch(`/api/employee/rent-directly/delete-room/${roomId}`, {
        method: 'delete',
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(res => res.json()).then(data => {
        let room;
        if (data.code === 200) {
            room = document.getElementById(`tr-room-${roomId}`)
            room.style.display = 'none'
            if (data['total_room'] === 1) {
                disabledDelRoomButton()
            }

            let txtRoomNumbers = ''
            let roomNumbers = document.getElementById('room_number')
            for (let i = 0; i < data['room_numbers'].length; i++)
                txtRoomNumbers += `${data['room_numbers'][i]}, `
            roomNumbers.innerText = txtRoomNumbers
        }
    }).catch(error => console.log(error))
}

// disabled button xoa phong
function disabledDelRoomButton() {
    let btnDelRoom = document.getElementsByClassName('btn-del-room')
    for (let i = 0; i < btnDelRoom.length; i++)
        btnDelRoom[i].disabled = true;
}

// refresh session rent directly
function cleanRentDirectlyInSession(){
     fetch('/api/employee/rent-directly/clean-book-room', {
        method: 'delete',
    }).then(res => res.json()).then(data => {
        if (data.code === 200) {
            location.reload()
        }
    }).catch(error => error => console.log(error))
}