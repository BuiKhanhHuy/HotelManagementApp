// them binh luan
function addComment(room_id) {
    let textArea = document.getElementById(`comment-${room_id}`)
    let content = textArea.value

    fetch('/api/customer/add_comment', {
        method: 'post',
        body: JSON.stringify({
            'room_id': room_id,
            'content': content,
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(res => res.json()).then(data => {
        if (data.code === 200) {
            if (data.success === true) {
                let divComment = document.getElementById('comment')
                let sessionComment = divComment.innerHTML

                sessionComment = getHTMLComment(data['comments'], data['user']) + sessionComment
                divComment.innerHTML = sessionComment
            } else {
                alert(data['error'])
            }
        }
    }).catch(error => error => console.log(error))
}

// hien thi binh luan moi
function getHTMLComment(comment, user) {
    return `<div class="media p-3"> <img src="${user['avatar']}" alt="avt"
                     class="mr-3 mt-3 rounded-circle" style="width:60px;">
                    <div class="media-body">
                        <h4>${user['username']}
                        <small>
                            <i>${moment(comment['created_date']).locale('vi').fromNow()}</i>
                        </small>
                        </h4>
                        <p>${comment['content']}</p>
                    </div>
                </div>`
}


// chuyen trang binh luan
function getHTMLCommentAll(commentList) {
    return `
         <div class="media p-3">
            <img src="${commentList['avatar']}" alt="John Doe"
                 class="mr-3 mt-3 rounded-circle" style="width:60px;">
            <div class="media-body">
                <h4>${commentList['user_name']}<small
                        class="pl-1"><i>${moment(commentList['created_date']).locale('viz').fromNow()}</i></small></h4>
                <p>${commentList['content']}</p>
            </div>
        </div>
    `
}


// lay html pagination comment
function getHTMLCommentPagination(roomId, iter_pages, page) {
    let iterPages = document.getElementById('custom-pagination')
    let lis = ''

    for (let i = 0; i < iter_pages.length; i++) {
        if (iter_pages[i] == null)
            lis += ` <li><a class="text-warning"
                                       href="javascript:void(0)">...</a>
                                </li>`
        else {
            if (page === iter_pages[i]) {
                lis += `<li><a class="text-white bg-warning" onclick="moveComment(${roomId} , ${iter_pages[i]})"
                                       href="javascript:void(0)"> ${iter_pages[i]}</a>
                                </li>`
            } else
                lis += `<li><a class="text-warning" onclick="moveComment(${roomId} , ${iter_pages[i]})"
                                       href="javascript:void(0)"> ${iter_pages[i]}</a>
                                </li>`
        }

    }
    iterPages.innerHTML = lis
}


// move comment
function moveComment(roomId, page) {
    fetch('/api/customer/load_comments', {
        method: 'post',
        body: JSON.stringify({
            'room_id': roomId,
            'page': page
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(res => res.json()).then(data => {
        if (data.code === 200) {
            let commentContent = document.getElementById('comment')
            let txtContent = ''

            for (let i = 0; i < data['comment_list'].length; i++) {
                txtContent += getHTMLCommentAll(data['comment_list'][i])
            }
            commentContent.innerHTML = txtContent
            console.log(txtContent)
            getHTMLCommentPagination(roomId, data['iter_pages'], page)
        }
    }).catch(error => error => console.log(error))
}