// show book room modal
function showModal(textTitle, textBody) {
    document.getElementById('id-modal-title').innerText = textTitle
    document.getElementById('id-modal-body').innerText = textBody
    $("#my-modal").modal({show: true});
}