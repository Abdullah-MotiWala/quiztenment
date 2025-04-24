let modal_response_data = {}

$(document).on('click', '#store_likes_btn', function(){
    var data = $(this)
    let csrfmiddlewaretoken = $("input[name = 'csrfmiddlewaretoken']").val()
    var product_id = data.attr("data-product-id")
    $.ajax({
        method : 'POST' , 
        url : "/product_like_api/" + product_id ,
        data : {"csrfmiddlewaretoken" : csrfmiddlewaretoken} ,
            dataType : "json",
            success : function(response){

            console.log(response.product_like_count)
            if(response){
                $(".product_like_count-" + product_id).html("")
                $(".product_like_count-" + product_id).html(response.product_like_count)
            }
            },
            error: function(error){
            console.log("error")
            console.log(error)



        }                
    })    






});// end function jQuery 



