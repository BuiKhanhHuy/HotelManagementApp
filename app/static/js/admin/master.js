window.onload = function (){
    changeContentHeight()
}

window.onresize = function () {
    changeContentHeight()
}

function changeContentHeight() {
    var widthNav = document.getElementById('my-nav')
    var content = document.getElementById('my-content')
    content.style.height = (window.innerHeight - widthNav.clientHeight * 1.75) + "px"
}