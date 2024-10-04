/*
Ana Vitkovic 0285/2021
*/

function getCSRFToken() {
    let name = "csrftoken="
    let decodedCookie = decodeURIComponent(document.cookie);
    let ca = decodedCookie.split(";");
    for (let i = 0; i < ca.length; i++) {
        let c = ca[i];
        while (c.charAt(0) == ' ') {
            c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
            return c.substring(name.length, c.length);
        }
    }
    return "";
}
function removePupUp() {
    $('.alert').removeClass("show");
    $('.alert').addClass("hide");
}


$(document).ready(function(){

    $('.close-btn').click(removePupUp);

    // sending ajax request when we want to rate plan
    $("#submit_rate_btn_plan").click(function () {

        let checkedRadio = document.querySelector('input[name="rate"]:checked');
        if(!checkedRadio) return;

        fetch("rate-plan", {
            method: "POST",
            headers: {
                "Content-Type" : "application/json",
                "X-CSRFToken" : getCSRFToken()
            },
            body: JSON.stringify(checkedRadio.value),
        }).then(
            response => {
                 $('.alert').addClass("show");
                 $('.alert').removeClass("hide");
                 $('.alert').addClass("showAlert");
                if (response.status == 200) {
                    response.text().then(
                    response =>$("#averageRating").html(response));
                    $('.alert').removeClass("error-col");
                    $(".my-bx").removeClass("bxs-error-circle");
                    $(".my-bx").addClass("bxs-check-circle");
                    $('.msg').html("Success: Your rate has been submitted!");
                    $(".alert").addClass("success-col");
                }
                setTimeout(removePupUp,5000);
            }
        )
    });

    $("#submit_rate_btn_nutri").click(function () {

        let checkedRadio = document.querySelector('input[name="rate"]:checked');
        if(!checkedRadio) return;

        fetch("rate-nutri", {
            method: "POST",
            headers: {
                "Content-Type" : "application/json",
                "X-CSRFToken" : getCSRFToken()
            },
            body: JSON.stringify(checkedRadio.value),
        }).then(
            response => {
                 $('.alert').addClass("show");
                 $('.alert').removeClass("hide");
                 $('.alert').addClass("showAlert");
                if (response.status == 200) {
                    response.text().then(
                    response =>$("#averageRating").html(response));
                    $('.alert').removeClass("error-col");
                    $(".my-bx").removeClass("bxs-error-circle");
                    $(".my-bx").addClass("bxs-check-circle");
                    $('.msg').html("Success: Your rate has been submitted!");
                    $(".alert").addClass("success-col");
                }
                setTimeout(removePupUp,5000);
            }
        )
    });

    $("#download_plan_btn").click(function () {

        fetch("download-plan", {
            method: "POST",
            headers: {
                "Content-Type" : "application/json",
                "X-CSRFToken" : getCSRFToken()
            },
        }).then(
            response => {
                 $('.alert').addClass("show");
                 $('.alert').removeClass("hide");
                 $('.alert').addClass("showAlert");
                if (response.status == 200) {
                    response.text().then(
                    response =>$("#averageRating").html(response));
                    $('.alert').removeClass("error-col");
                    $(".my-bx").removeClass("bxs-error-circle");
                    $(".my-bx").addClass("bxs-check-circle");
                    $('.msg').html("Success: The pan has been downloaded!");
                    $(".alert").addClass("success-col");
                }
                else if(response.status==201){
                    response.text().then(
                    response =>$("#averageRating").html(response));
                    $('.alert').removeClass("error-col");
                    $(".my-bx").removeClass("bxs-error-circle");
                    $(".my-bx").addClass("bxs-info-circle");
                    $('.msg').html("Warning: You have already downloaded the plan");
                    $(".alert").addClass("warning-col");
                }
                setTimeout(removePupUp,5000);
            })

    });

});


