function add_to_book_room(room_id,room_number,
    kind_of_room_name,price){

    fetch('/api/booking/add-to-book-room-cart',{
        method:'post',
        body: JSON.stringify({
            'room_id' : room_id,
            'room_number' : room_number,
            'kind_of_room_name' : kind_of_room_name,
            'price' :  price
        }),
        headers:{
            'Content-Type':'application/json'
        }
    }).then(function(res){
        console.info(res)
        return res.json()
    }).then(function(data){
        console.info(data)
        let  counter = document.getElementById('cusCartCounter')
        counter.innerText = data.total_room
    }).catch(function(err){
       alert("Lỗi:" + err)
    })

}
function cal_day(d1, d2){
   var t2 = d2.getTime();
   var t1 = d1.getTime();

   return Math.floor((t2-t1)/(24*3600*1000));
}
function del_cus_cart_booking(room_id){
    if(confirm("Bạn có chắc chắn xóa phòng này khỏi giỏ hàng không?") == true){
        fetch('/api/delete-cart-booking/'+room_id,{
            method:'delete',
            headers:{
                'Content-Type':'application/json'
            }
        }).then(function(res){
            console.info(res)
            return res.json()
        }).then(function(data){
            console.info(data)
            let  counter = document.getElementById('cusCartCounter')
            let  counter2 = document.getElementById('total')
            counter.innerText = data.total_room
            counter2.innerText = data.total_room


            let e = document.getElementById("room" + room_id)
            e.style.display = "none"
        }).catch(function(err){
           console.log("Lỗi:" + err)
        })
    }
}