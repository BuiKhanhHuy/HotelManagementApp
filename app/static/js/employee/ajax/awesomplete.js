// goi y cmnd va dien thong tin khach hang o phan xac nhan dat phong
document.addEventListener('DOMContentLoaded', () => {
    const input = document.querySelector('input.identification-card');
    const awesomplete = new Awesomplete(input);

    input.addEventListener('keyup', (e) => {
        var code = (e.keyCode || e.which);
        let valueInput = ''
        valueInput = input.value.toString()

        if (code >= 65 && code <= 90 || code >= 97 && code <= 105 || code >= 48 && code <= 57) {
            fetch(`/api/employee/get-identification_card`, {
                method: 'post',
                body: JSON.stringify({
                    'id_value': valueInput
                }),
                headers: {
                    'Content-Type': 'application/json'
                }
            }).then(res => res.json()).then(data => {
                if (data.code === 200) {
                    // console.log(data['identification_cards'])
                    awesomplete.list = data['identification_cards']
                }
            }).catch(error => console.log(error))
        } else {
            if (code === 13) {
                // khi nguoi dung chon duoc cmnd co san
                loadCustomerFromIdCard(valueInput)
                return 0;
            }
        }
    });

    input.addEventListener(`awesomplete-selectcomplete`, (e) => {
        let valueInput = ''
        valueInput = input.value.toString()
        loadCustomerFromIdCard(valueInput)
    });
});

// lay thong tin khach hang thong qua cmnd
function loadCustomerFromIdCard(id_card) {
    fetch(`/api/employee/get-customer`, {
        method: 'post',
        body: JSON.stringify({
            'id_card': id_card
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(res => res.json()).then(data => {
        if (data.code === 200) {
            if (data['customer']) {
                // lay duoc thong tin khach hang tu id_card
                console.log('Load khach hang ra form')
                loadCustomerIntoForm(data['customer'])
            } else {
                // khong tim duoc khach hang do gt = null
                console.log('Lay thông tin khach hang moi, khach hang nhap thong tin.')
                return 0;
            }
        }
    }).catch(error => console.log(error))
}

