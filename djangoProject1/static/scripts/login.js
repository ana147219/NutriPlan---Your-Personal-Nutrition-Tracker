/*
Tijana Gasic 0247/2021
Natasa Spasic 0310/2021
*/

$(document).ready(function() {

    $('#reset-code-forgot-pass').click(function(event) {
            event.preventDefault();
            console.log($('#email2').val())
            $.ajax({
                url: '/resend-code-forgot-pass/',
                type: 'POST',
                data: {
                    'email': $('#email2').val(),
                    'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()
                },
                success: function(response) {
                    //alert(response.message);
                },
                error: function(xhr, errmsg, err) {
                    //alert('Error resending code. Please try again.');
                }
            });
        });
    $('#reset-code-signup').click(function(event) {
            event.preventDefault();
            $.ajax({
                url: '/resend-code-signup/',
                type: 'POST',
                data: {
                    'username': $('#username').val(),
                    'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()
                },
                success: function(response) {
                    //alert(response.message);
                },
                error: function(xhr, errmsg, err) {
                    //alert('Error resending code. Please try again.');
                }
            });
        });

    function sign_up(event){
        window.location.href = "user.html";
    }


    function go_to_user_page(event){
        window.location.href = "user.html";
    }

    const wrapper=document.querySelector('.wrapper');
    const registerLink0= document.querySelector('.register-link0');

    registerLink0.onclick= () => {

        wrapper.classList.add('active');
    }

    const loginLink1=document.querySelector('.login-link1');

    loginLink1.onclick= () => {

        wrapper.classList.remove('active');


    }

    $(document).keypress(function(event) {
        if (event.key === 'Enter') {
            if ($(".wrapper").hasClass("active")) {
                event.preventDefault(); // Prevent the default form submission
            }
        }
    });

    const next1=document.querySelector('.next1');

    next1.onclick= () => {
        if ($('#usernameText').text() != '' || $('#emailText').text().trim() != '' || $('#confPassText').text().trim() != '') {
            $('.alert').addClass("show");
            $('.alert').removeClass("hide");
            $('.alert').removeClass("warning-col");
            $('.alert').addClass("showAlert");
            $('.msg').html("Please fix the errors before proceeding.");
            $(".alert").addClass("error-col");

            setTimeout(function(){
              $('.alert').removeClass("show");
              $('.alert').addClass("hide");

            },5000);
            return;
        }
        if ($('#username').val() == '' || $('#email').val() == '' || $('#password').val() == '' || $('#confirmpassword').val() == '') {
            $('.alert').addClass("show");
            $('.alert').removeClass("hide");
            $('.alert').removeClass("error-col");
            $('.alert').addClass("showAlert");
            $('.msg').html("Warning: Must fill out every field!");
            $(".alert").addClass("warning-col");

            setTimeout(function(){
              $('.alert').removeClass("show");
              $('.alert').addClass("hide");

            },5000);
            return;
        }

        wrapper.classList.remove('active');
        wrapper.classList.add('active1');


    }


    const loginLink2=document.querySelector('.login-link2');

    loginLink2.onclick= () => {

        wrapper.classList.remove('active1');


    }


    const next2=document.querySelector('.next2');

    next2.onclick= () => {

        wrapper.classList.remove('active1');
        wrapper.classList.add('active2');


    }




    const loginLink3=document.querySelector('.login-link3');

    loginLink3.onclick= () => {

        wrapper.classList.remove('active2');


    }




    const fpLink=document.querySelector('.fp-link');


    fpLink.onclick= () => {

        wrapper.classList.add('fp');
    }




    const loginLink4=document.querySelector('.login-link4');

    loginLink4.onclick= () => {

        wrapper.classList.remove('fp');


    }


    const next4=document.querySelector('.next4');

    next4.onclick= () => {
        console.log("next4")

        if ( $('#emailText2').text().trim() != '' || $('#confPassText2').text().trim() != '') {
            $('.alert').addClass("show");
            $('.alert').removeClass("hide");
            $('.alert').removeClass("warning-col");
            $('.alert').addClass("showAlert");
            $('.msg').html("Please fix the errors before proceeding.");
            $(".alert").addClass("error-col");

            setTimeout(function(){
              $('.alert').removeClass("show");
              $('.alert').addClass("hide");

            },5000);
            return;
        }
        if ($('#email2').val() == '' || $('#password2').val() == '' || $('#confirmpassword2').val() == '') {
            $('.alert').addClass("show");
            $('.alert').removeClass("hide");
            $('.alert').removeClass("error-col");
            $('.alert').addClass("showAlert");
            $('.msg').html("Warning: Must fill out every field!");
            $(".alert").addClass("warning-col");

            setTimeout(function(){
              $('.alert').removeClass("show");
              $('.alert').addClass("hide");

            },5000);
            return;
        }
        $.ajax({
                    type: 'POST',
                    url: '/forgot-password',
                    data: {
                        email: $('#email2').val(),
                        password: $('#password2').val(),
                        csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
                    }
                })

        wrapper.classList.remove('fp');
        wrapper.classList.add('fp1');


    }


    const loginLink5=document.querySelector('.login-link5');

    loginLink5.onclick= () => {

        wrapper.classList.remove('fp1');


    }

    $('.close-btn').click(function(){
    $('.alert').removeClass("show");
    $('.alert').addClass("hide");
    });


});


