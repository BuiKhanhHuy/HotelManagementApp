// show book room modal
function showBookRoomModal(textTitle, textBody) {
    document.getElementById('id-modal-title').innerText = textTitle
    document.getElementById('id-modal-body').innerText = textBody
    $("#bookRoomModal").modal({show: true});
}