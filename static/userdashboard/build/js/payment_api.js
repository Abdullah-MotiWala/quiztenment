let modal_response_data = {}

$(document).on('click', '#send_payment_detail', function(){
    
    var payment_type = $( "#payment_type option:selected" ).val();
    var email_addr = $( "#email_addr").val();
    var mobile_number = $( "#mobile_number").val();
    var cnic = $( "#cnic").val()
    let csrfmiddlewaretoken = $("input[name = 'csrfmiddlewaretoken']").val()


    var user_data = {
        payment_type  : payment_type,
        email_addr  : email_addr,
        mobile_number  : mobile_number,
        cnic  : cnic,
    }

	var payment_url = " https://pay-sandbox.link.com.pk/?"
	var api_key = "43AF0AB3C51C82B2BA17E483F5C007FA&"
	var merchant_id = "QT40001&"  
	var item = "test&"   
	var amount = "1&"
	var checksum = "ca8b3cd9697ca98b91f59efb32314b9cb383e8aa54747ba0a8702f81889a7e58" 
	var secrat_key = "E3DC8F93C49E386B"
	var mrul = payment_url + api_key + merchant_id + item + amount + checksum	
    $.ajax({
        method : 'POST' , 
        url : mrul ,
        dataType : "json",
        data : 
        {
            "csrfmiddlewaretoken" : csrfmiddlewaretoken , 
            "data" : user_data , 
        } 

        data : JSON.stringify(data),
        success : function(response){
        if(response){
            console.log(" Test Response   " + JSON.stringify(response))
        }
        },
        error: function(error){
        console.log("error")
        console.log(error)
        }                
    })    






});// end function jQuery 



$(document).on('click', '#store_dis_likes_btn', function(){
    var data = $(this)
    let csrfmiddlewaretoken = $("input[name = 'csrfmiddlewaretoken']").val()
    var product_id = data.attr("data-product-id")
    $.ajax({
        method : 'POST' , 
        url : "/product_dislike_api/" + product_id ,
        data : {"csrfmiddlewaretoken" : csrfmiddlewaretoken} ,
            dataType : "json",
            success : function(response){

            console.log(response.product_like_count)
            if(response){
                $(".product_dislike_count-" + product_id).html("")
                $(".product_dislike_count-" + product_id).html(response.product_dislike_count)
            }
            },
            error: function(error){
            console.log("error")
            console.log(error)



        }                
    })    






});// end function jQuery 




$(document).on('click', '#store_playlist_btn', function(){
    var data = $(this)
    let csrfmiddlewaretoken = $("input[name = 'csrfmiddlewaretoken']").val()
    var product_id = data.attr("data-product-id")

    $.ajax({
        method : 'POST' , 
        url : "/product_playist_api/" + product_id ,
        data : {"csrfmiddlewaretoken" : csrfmiddlewaretoken} ,
            dataType : "json",
            success : function(response){
            console.log("store_playlist_btn Response " +  JSON.stringify(response))
            if(response){
                if(response.success && response.product_playlist_status == 1){
                    console.log(" store_playlist_btn  ")
                    $(".data-playlist-product-id-" + product_id).removeClass("fa-plus")
                    $(".data-playlist-product-id-" + product_id).addClass("fa-check")    
                }
            }
            },
            error: function(error){
            console.log("error")
            console.log(error)



        }                
    })    





});// end function jQuery 



$(document).ready(function () {

    $(document).on("click", ".open-AddDialog", function () {
    var myBookId = $(this).data('id');
    $(".modal-body #bookId").val( myBookId );
    // As pointed out in comments, 
    // it is unnecessary to have to manually call the modal.
    // $('#addBookDialog').modal('show');
});
});



$(document).on('click', '.open-AddDialog', function(){
    var data = $(this)
    var product_id = data.attr("data-product-id")
    let csrfmiddlewaretoken = $("input[name = 'csrfmiddlewaretoken']").val()
    $.ajax({
        method : 'POST' , 
        url : "/product_detail/" + product_id ,
        data :{"product_id" : product_id ,  csrfmiddlewaretoken: csrfmiddlewaretoken },

        dataType : "json",
        success : function(response){
        console.log("modal Response " +  JSON.stringify(response))
        
        if(response){
            if(response.success){
                modal_response_data = response.data
                let collection_dropdown = []
                let html_collection_dropdown = ""
                let product_collections = []
                let modal_project_droopdown_key = ""
                // $("#product_trailer_video").attr("src", )

                

                for(var key in modal_response_data){
                    if (modal_project_droopdown_key == ""){
                        modal_project_droopdown_key = key
                    }
                    html_collection_dropdown += "<option data-project-name-key  = '"+key+"'  value='"+modal_response_data[key].project_id+"'> "+ key.replace(/_/g, " ") +" </option> "
                    // console.log(key)
                    // console.log( data[key].project_id)
                    // row = {"project_id" :  data[key].project_id , project_name  :  key.replace(/_/g, " ")}
                    // collection_dropdown.push(row)

                }
                console.log("-----   modal_response_data -   " + JSON.stringify(modal_response_data)  )

                // console.log(JSON.stringify(collection_dropdown))
                



                $(".modal_project_droopdown").html(html_collection_dropdown);

                var select_value_key = $('option:selected', ".modal_project_droopdown").attr('data-project-name-key');
                console.log(modal_project_droopdown_key + " modal_project_droopdown_key")

                var project_product_table = modal_response_data[modal_project_droopdown_key].project_product
                console.log(" project_product_table "  + JSON.stringify(project_product_table))
                set_html_modal_project_dropdown(project_product_table , product_id)
            
                $('.modal').modal('show');
            }
            // var myBookId = $(this).data('id');
        

            // if(response.success && product_playlist_status == 1){

            //     console.log(" store_playlist_btn  ")
            //     $(".data-playlist-product-id=-" + product_id).removeClass("bi-plus-circle")
            //     $(".data-playlist-product-id=-" + product_id).addClass("bi-check-circle-fill")    
            // }
        }
        
        },
        error: function(error){
        console.log("error")
        console.log(error)
        }                
    })
});// end function jQuery 








$(document).on("change", ".modal_project_droopdown", function () {
    var data = $(this)
    var select_value_key = $('option:selected', this).attr('data-project-name-key');
    var select_value = $('.modal_project_droopdown').val();
    var project_product_table = modal_response_data[select_value_key].project_product
    set_html_modal_project_dropdown(project_product_table)







    console.log(select_value)
    console.log(select_value_key)


});

function set_html_modal_project_dropdown(project_product , product_id){
    console.log("set_html_modal_project_dropdown called. ")
    $(".modal_project_table").html()
    let modal_table_design = ``
    var counter = 0
    var product_trailer = ""
    $.each(project_product,function(key,value){
        counter++
        modal_table_design += `
        <tr style="border:1px solid gray">
        <td class="align-middle" > `+counter+` </td>
                <td class="align-middle">
                <a href="/play_video/`+value.id+`">
                <img src="`+value.product_poster+`" class="card-img-top" alt="...">
                </a>
                </td>
                <td> 
                    <div class=" d-flex justify-content-between"> 
                        <div> `+value.product_name+` </div>
                        <div> Date 24 March </div>
                    </div>
                    <p class="text-justify p-2 px-4 ">
                        Lorem ipsum dolor sit amet consectetur adipisicing elit. Modi explicabo dolorput perferendis provident, temporibus qui vero , sed  proectus   stiae? Neque, alias! Illum quae velit laboriosam explicabo ipsa tenetur
                        inventore corporis et, qui minus accusamus fuga odit sus
                    </p>
                </td>
                </tr>
            `
            if (value.id == product_id){
                console.log('Yes Product id and Value ID Matched. ')
                console.log('product_trailer --  ' + value.product_trailer)
                product_trailer = value.product_trailer
                $(".model_product_name").html(value.project_name);
            }



      })// each loop end. 


    console.log("product_trailer === " + product_trailer )
      $(".modal_project_table").html(modal_table_design)


    

}