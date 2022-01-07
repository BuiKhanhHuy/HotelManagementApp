// in phieu dat phong
function printBookingForm() {
    let removePrints = document.getElementsByClassName('remove-print')
    let removePrintButtons = document.getElementsByClassName('bt-print-page')
    let element = document.getElementById("myDIV");

    // xoa cac thanh phan khong can thiet
    element.classList.remove("page-wrapper");
    for (let i = 0; i < removePrints.length; i++)
        removePrints[i].style.display = 'none'
    for (let i = 0; i < removePrintButtons.length; i++)
        removePrintButtons[i].style.display = 'none'

    // in
    window.print()

    // cap nhap lai cac thanh phan da xoa
    element.classList.add("page-wrapper");
    for (let i = 0; i < removePrints.length; i++)
        removePrints[i].style.display = 'block'
    for (let i = 0; i < removePrintButtons.length; i++)
        removePrintButtons[i].style.display = 'inline'
}