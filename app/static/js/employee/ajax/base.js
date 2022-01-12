// show book room modal
function showModal(textTitle, textBody) {
    document.getElementById('id-modal-title').innerText = textTitle
    document.getElementById('id-modal-body').innerText = textBody
    $("#my-modal").modal({show: true});
}

// hien thi notification
function notification(type, text) {
    let txtText = ""
    switch (type) {
        case 1:
            txtText = "success";
            break;
        case 2:
            txtText = "error";
            break;
        case 3:
            txtText = "warning";
            break;
        case 4:
            txtText = "info";
            break;
    }
    $.notify(text, txtText);
}