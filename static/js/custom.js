function sendArticleComment(articleId) {
    var comment = $('#reply-message').val();
    var parentId = $('#parent_id').val();
    console.log(parentId);
    $.get('/articles/add-article-comment', {
        article_comment: comment,
        article_id: articleId,
        parent_id: parentId
    }).then(res => {
        $('#comments_area').html(res);
        $('#reply-message').val('');
        $('#parent_id').val('');

        if (parentId !== null && parentId !== '') {
            document.getElementById('single_comment_box_' + parentId).scrollIntoView({behavior: "smooth"});
        } else {
            document.getElementById('comments_area').scrollIntoView({behavior: "smooth"});
        }
    });
}

function fillParentId(parentId) {
    $('#parent_id').val(parentId);
    document.getElementById('comment_form').scrollIntoView({behavior: "smooth"});
}


function filterProducts(){
    const filterPrice = $('#price_range').val();
    const start_price = filterPrice.split(',')[0];
    const end_price = filterPrice.split(',')[1];
    $('#start_price').val(start_price);
    $('#end_price').val(end_price);
    $('#filter_form').submit();

}
function fillPage(){
    $('#page').val(page);
    $('#filter_form').submit();


}


function showLargeImage(imageSrc){
    console.log(imageSrc);
    $('#product-zoom').attr('src',imageSrc);
    $('#btn-product-gallery').attr('href',imageSrc);

}

function addProductToOrder(productId) {
    const productCount = $('#qty').val();
    $.get('/order/add-to-order?product_id=' + productId + '&count=' + productCount).then(res => {
         Swal.fire({
            title: 'اعلان',
            text: res.text,
            icon: res.icon,
            showCancelButton: false,
            confirmButtonColor: '#3085d6',
            confirmButtonText: res.confirm_button_text
        }).then((result) => {
            if (result.isConfirmed && res.status === 'not_auth') {
                window.location.href = '/login';
            }
        })


        /*if (res.status === 'success') {
            Swal.fire({
                title: 'اعلان',
                text: "محصول مورد نظر با موفقیت به سبد خرید شما اضافه شد",
                icon: 'success',
                showCancelButton: false,
                confirmButtonColor: '#3085d6',
                confirmButtonText: 'باشه ممنون'
            });
        } else if (res.status === 'not_found') {
            Swal.fire({
                title: 'اعلان',
                text: "محصول مورد نظر یافت نشد",
                icon: 'error',
                showCancelButton: false,
                confirmButtonColor: '#3085d6',
                confirmButtonText: 'باشه ممنون'
            });
        }*/
    });
}


function removeOrderDetail(detailId) {
    $.get('/user/remove-order-detail?detail_id=' + detailId).then(res => {
        if (res.status === 'success') {
            $('#order-detail-content').html(res.body);
        }
    });
}


// detail id => order detail id
// state => increase , decrease
function changeOrderDetailCount(detailId, state) {
    $.get('/user/change-order-detail?detail_id=' + detailId + '&state=' + state).then(res => {
        if (res.status === 'success') {
            $('#order-detail-content').html(res.body);
        }
    });
}
