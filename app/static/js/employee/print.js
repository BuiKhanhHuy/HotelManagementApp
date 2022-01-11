// remove cac thanh phan thua
function removeRedundancyBase() {
    let removePrints = document.getElementsByClassName('remove-print')
    let removePrintButtons = document.getElementsByClassName('bt-print-page')
    let element = document.getElementById("myDIV");

    // xoa cac thanh phan khong can thiet
    element.classList.remove("page-wrapper");
    for (let i = 0; i < removePrints.length; i++)
        removePrints[i].style.display = 'none'
    for (let i = 0; i < removePrintButtons.length; i++)
        removePrintButtons[i].style.display = 'none'
}

// add lai cac thanh phan da remove
function addBase() {
    let removePrints = document.getElementsByClassName('remove-print')
    let removePrintButtons = document.getElementsByClassName('bt-print-page')
    let element = document.getElementById("myDIV");

    // cap nhap lai cac thanh phan da xoa
    element.classList.add("page-wrapper");
    for (let i = 0; i < removePrints.length; i++)
        removePrints[i].style.display = 'flex'
    for (let i = 0; i < removePrintButtons.length; i++)
        removePrintButtons[i].style.display = 'inline'
}

// in phieu dat phong
function printBookingForm() {
    // xoa di
    removeRedundancyBase()
    // in
    window.print()
    // add lai
    addBase()
}

// in phieu thue phong
function printRentRoom() {
    let removeClass = document.getElementsByClassName('remove-class')
    // xoa di
    removeRedundancyBase()
    for (let i = 0; i < removeClass.length; i++) {
        removeClass[i].classList.remove("overflow-auto");
        removeClass[i].style.height = "auto"
    }

    // in
    window.print()

    // add lai
    addBase()
    for (let i = 0; i < removeClass.length; i++) {
        removeClass[i].classList.add("overflow-auto");
        removeClass[i].style.height = "400px";
    }
}