(function ($) {
    "use strict";

    /*Start Registration Form*/
    $(window).on("load", function(){
        $('#registrationbtn').on('click', function() {


            $('#registrationbtn').html('Sending..');

            var checkformval  = $('#checkformval').val();
            var activation_code  = $('#activation_code').val();
            var first_name = $("#first_name").val();
            var last_name = $("#last_name").val();
            var user_name = $("#user_name").val();
            var user_password = $("#user_password").val();
            var email = $("#email").val();
            var phone_number = $("#phone_number").val();
            var city = $("#city").val();
            var cnic_number = $("#cnic_number").val();
            var acceptterms = $("#acceptterms").val();


            $.ajax({
                url: $(this).closest("form").attr("action"),
                type: $(this).closest("form").attr("method"),
                dataType: "json",
                data: {
                    checkformval: checkformval,
                    activation_code: activation_code,
                    first_name:first_name,
                    last_name: last_name,
                    user_name: user_name,
                    user_password: user_password,
                    email: email,
                    phone_number: phone_number,
                    city: city,
                    cnic_number: cnic_number,
                    acceptterms: acceptterms,
                },
                success: function(data) {
                    if (data.regsuccess) {
                        $('#registrationbtn').html('Submit Now');
                        $(".reg-alert-danger").css('display', 'none');
                        $(".reg-alert-success").css('display', 'block');

                        window.setTimeout(function() {
                            window.location.href = base_url+"signin/index"
                        }, 1500)

                        $(".reg-alert-success").html(data.regsuccess);
                    } else {
                        $('#registrationbtn').html('Submit Now');
                        $(".reg-alert-danger").css('display', 'block');
                        $(".reg-alert-danger").html(data.regerror);
                        //alert(data.error);
                    }
                }
            });

            //return false;
        });

    });
    /*End Registration Form*/

    /*Start Registration Form*/
    $(window).on("load", function(){
        $('#guestformbtn').on('click', function() {


            $('#guestformbtn').html('Sending..');

            var checkformval  = $('#checkformval').val();
            var guest_name = $("#guest_name").val();
            var guest_email = $("#guest_email").val();
            var guest_phone_number = $("#guest_phone_number").val();
            var city = $("#city").val();
            var guest_email = $("#guest_email").val();
            var guest_phone_number = $("#guest_phone_number").val();


            $.ajax({
                url: $(this).closest("form").attr("action"),
                type: $(this).closest("form").attr("method"),
                dataType: "json",
                data: {
                    checkformval: checkformval,
                    guest_name: guest_name,
                    guest_email:guest_email,
                    guest_phone_number: guest_phone_number,
                    city: city,
                    guest_email: guest_email,
                    guest_phone_number: guest_phone_number
        
                },
                success: function(data) {
                    if (data.regsuccess) {
                        $('#guestformbtn').html('Submit Now');
                        $(".reg-alert-danger").css('display', 'none');
                        $(".reg-alert-success").css('display', 'block');

                        window.setTimeout(function() {
                            window.location.href = base_url+"signin/index"
                        }, 1500)

                        $(".reg-alert-success").html(data.regsuccess);
                    } else {
                        $('#guestformbtn').html('Submit Now');
                        $(".reg-alert-danger").css('display', 'block');
                        $(".reg-alert-danger").html(data.regerror);
                        //alert(data.error);
                    }
                }
            });

            //return false;
        });

    });
    /*End Registration Form*/

    /*EMail Activation*/
    $(window).on("load", function(){
        $('#emailactivation').on('click', function() {


            $('#emailactivation').html('Sending..');

            var checkformval  = $('#checkformval').val();
            var activation_code  = $('#submit_email_active').val();



            $.ajax({
                url: $(this).closest("form").attr("action"),
                type: $(this).closest("form").attr("method"),
                dataType: "json",
                data: {
                    checkformval: checkformval,
                    activation_code: activation_code,

                },
                success: function(data) {
                    if (data.activesuccess) {
                        $('#emailactivation').html('Submit Now');
                        $(".reg-alert-danger").css('display', 'none');
                        $(".reg-alert-success").css('display', 'block');

                        window.setTimeout(function() {
                            window.location.href = base_url+"signin/index"
                        }, 1500)

                        $(".reg-alert-success").html(data.activesuccess);
                    } else {
                        $('#emailactivation').html('Submit Now');
                        $(".reg-alert-danger").css('display', 'block');
                        $(".reg-alert-danger").html(data.activeerror);
                        //alert(data.error);
                    }
                }
            });

            //return false;
        });

    });

    /*Forgot Password*/
    $(window).on("load", function(){
        $('#forgotpasswordsubmit').on('click', function() {


            $('#forgotpasswordsubmit').html('Sending..');

            var checkformval  = $('#checkformval').val();
            var submit_forgot_password  = $('#submit_forgot_password').val();



            $.ajax({
                url: $(this).closest("form").attr("action"),
                type: $(this).closest("form").attr("method"),
                dataType: "json",
                data: {
                    checkformval: checkformval,
                    submit_forgot_password: submit_forgot_password,

                },
                success: function(data) {
                    if (data.activesuccess) {
                        $('#forgotpasswordsubmit').html('Submit Now');
                        $(".reg-alert-danger").css('display', 'none');
                        $(".reg-alert-success").css('display', 'block');

                        window.setTimeout(function() {
                            window.location.href = base_url+"signin/index"
                        }, 1500)

                        $(".reg-alert-success").html(data.activesuccess);
                    } else {
                        $('#forgotpasswordsubmit').html('Submit Now');
                        $(".reg-alert-danger").css('display', 'block');
                        $(".reg-alert-danger").html(data.activeerror);
                        //alert(data.error);
                    }
                }
            });

            //return false;
        });

    });


    /*Set New Password*/
    $(window).on("load", function(){
        $('#submitnewpass').on('click', function() {


            $('#submitnewpass').html('Sending..');

            var checkformval  = $('#checkformval').val();
            var change_password  = $('#change_password').val();
            var submit_new_password  = $('#submit_new_password').val();



            $.ajax({
                url: $(this).closest("form").attr("action"),
                type: $(this).closest("form").attr("method"),
                dataType: "json",
                data: {
                    checkformval: checkformval,
                    change_password: change_password,
                    submit_new_password: submit_new_password,

                },
                success: function(data) {
                    if (data.activesuccess) {
                        $('#submitnewpass').html('Submit Now');
                        $(".reg-alert-danger").css('display', 'none');
                        $(".reg-alert-success").css('display', 'block');

                        window.setTimeout(function() {
                            window.location.href = base_url+"signin/index"
                        }, 1500)

                        $(".reg-alert-success").html(data.activesuccess);
                    } else {
                        $('#submitnewpass').html('Submit Now');
                        $(".reg-alert-danger").css('display', 'block');
                        $(".reg-alert-danger").html(data.activeerror);
                        //alert(data.error);
                    }
                }
            });

            //return false;
        });

    });

    /*Contact Us Form*/
    $(window).on("load", function(){
        $('#contactbtn').on('click', function(event) {
            event.preventDefault();

            $('#contactbtn').html('Sending..');

            var checkformval  = $('#checkformval').val();
            var contact_name  = $('#contact_name').val();
            var contact_phone_number  = $('#contact_phone_number').val();
            var contact_business_email  = $('#contact_business_email').val();
            var contact_subject_name  = $('#contact_subject_name').val();
            var contact_message  = $('#contact_message').val();

            $.ajax({
                url: $(this).closest("form").attr("action"),
                type: $(this).closest("form").attr("method"),
                dataType: "json",
                data: {
                    checkformval: checkformval,
                    contact_name: contact_name,
                    contact_phone_number: contact_phone_number,
                    contact_business_email: contact_business_email,
                    contact_subject_name: contact_subject_name,
                    contact_message: contact_message,

                },
                success: function(data) {
                    if (data.activesuccess) {
                        $('#contactbtn').html('Submit Now');
                        $(".reg-alert-danger").css('display', 'none');
                        $(".reg-alert-success").css('display', 'block');

                        window.setTimeout(function() {
                            window.location.href = base_url+"thankyou/index"
                        }, 1500)

                        $(".reg-alert-success").html(data.activesuccess);
                    } else {
                        $('#contactbtn').html('Submit Now');
                        $(".reg-alert-danger").css('display', 'block');
                        $(".reg-alert-danger").html(data.activeerror);
                        //alert(data.error);
                    }
                }
            });

            //return false;
        });

    });


})(jQuery);