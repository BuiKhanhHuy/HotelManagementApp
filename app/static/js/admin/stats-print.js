// ham print
function printStats(){
    let removePrint = document.getElementsByClassName('remove-print')
    let content = document.getElementById('my-content')
    let rows = document.getElementsByClassName('row-remove')
    let col6 = document.getElementsByClassName('col6')
    let col7 = document.getElementsByClassName('col7')
    let col5 = document.getElementsByClassName('col5')
    let title = document.getElementsByClassName('title')


    for(let i = 0; i < removePrint.length; i++)
        removePrint[i].style.visibility= 'hidden'

    content.classList.remove("overflow-auto", "shadow");

    for(let i = 0; i < rows.length; i++){
        rows[i].classList.remove('row')
    }

    for (let i = 0;i <  col6.length; i++)
    {
        col6[i].classList.remove('col-6')
        col6[i].classList.add('col-10', 'mx-auto', 'mb-4')
    }

    for (let i = 0;i <  title.length; i++)
    {
       title[i].classList.add('text-center')
    }

    col7[0].classList.remove('col-7')
    col7[0].classList.add('col-10', 'mx-auto', 'mb-4')

    col5[0].classList.remove('col-5')
    col5[0].classList.add('col-10', 'mx-auto')

    window.print()

    for(let i = 0; i < removePrint.length; i++)
        removePrint[i].style.visibility = 'visible';

    content.classList.add("overflow-auto", "shadow");

    for(let i = 0; i < rows.length; i++){
        rows[i].classList.add('row')
    }

    for (let i = 0;i <  col6.length; i++)
    {
        col6[i].classList.add('col-6')
        col6[i].classList.remove('col-10', 'mx-auto', 'mb-4')
    }

    for (let i = 0; i < title.length; i++)
    {
       title[i].classList.remove('text-center')
    }

    col7[0].classList.add('col-7')
    col7[0].classList.remove('col-10', 'mx-auto')

    col5[0].classList.add('col-5', 'mb-5')
    col5[0].classList.remove('col-10', 'mx-auto')
}