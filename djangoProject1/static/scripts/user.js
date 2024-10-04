$(document).ready(function () {


    var infinite = new Waypoint.Infinite({

    element: $('.infinite-container')[0],
    offset: 'bottom-in-view',
    onBeforePageLoad: function() {
    // Optional: Show loading indicator
    },
        onAfterPageLoad: function() {
        // Optional: Hide loading indicator
    }
    });





    window.addEventListener('pageshow', function(event) {
        if (event.persisted) {
            // Force a reload if the page is coming from cache
            window.location.reload();
        }
    });


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

    function myPlanLook() {
        window.location.href = "make-plan.html";
    }

    function myCurrentPlan() {
        window.location.href = "plan.html";
    }

    function createInput() {
        var formBox = document.createElement("div");
        formBox.classList.add("form-box", "login");

        var inputBox1 = document.createElement("div");
        inputBox1.classList.add("input-box", "animation");
        var input1 = document.createElement("input");
        input1.setAttribute("type", "text");
        input1.setAttribute("required", "");
        var label1 = document.createElement("label");
        label1.textContent = "Username";
        var icon1 = document.createElement("i");
        icon1.classList.add("bx", "bxs-user");
        inputBox1.appendChild(input1);
        inputBox1.appendChild(label1);
        inputBox1.appendChild(icon1);

        formBox.appendChild(inputBox1);

        var inputBox2 = document.createElement("div");
        inputBox2.classList.add("input-box", "animation");
        var input2 = document.createElement("input");
        input2.setAttribute("type", "password");
        input2.setAttribute("required", "");
        var label2 = document.createElement("label");
        label2.textContent = "Password";
        var icon2 = document.createElement("i");
        icon2.classList.add("bx", "bxs-lock-alt");
        inputBox2.appendChild(input2);
        inputBox2.appendChild(label2);
        inputBox2.appendChild(icon2);

        formBox.appendChild(inputBox2);

        return formBox;
    }

    var coll = document.getElementsByClassName("collapsible");
    var i;

    for (i = 0; i < coll.length; i++) {
        coll[i].addEventListener("click", function () {
            this.classList.toggle("active");
            var content = this.nextElementSibling;
            if (content.style.maxHeight) {
                content.style.maxHeight = null;
                //document.getElementById("my-content").innerHtml = "";
            } else {
                content.style.maxHeight = content.scrollHeight + "px";
                //console.log("ovde");
                //document.getElementById("my-content").appendChild(createInput());
            }
        });
    }


    /* circle progress bar */


    let options = {
        startAngle: -1.55,
        size: 150,
        value: document.getElementById("myData").textContent,
        /*fill: {gradient: ['#a445b2', '#fa4299']}*/

        fill: {gradient: ['#00aaff', '#a445b2']}
    }


    $(".circle .bar").circleProgress(options).on('circle-animation-progress',
        function (event, progress, stepValue) {
            var val;
            if (Number.isInteger(stepValue)) {
                stepValue*=100
                val = stepValue.toString();
            } else {
                stepValue*=100
                val = stepValue.toFixed(2);
                val = parseFloat(val).toString()
            }
            $(this).parent().find("span").text(val + "%");
        });


    /*

upload pic

     */

    const uploadInput = document.getElementById("upload_input");

    uploadInput.addEventListener("change", () => {

        if (uploadInput.files && uploadInput.files[0]) {

            var form_data = new FormData();
            form_data.append('file', uploadInput.files[0]);

            $.ajax({
                url: 'upload_profile_picture',
                method: 'POST',
                processData: false,
                contentType: false,
                mimeType: "multipart/form-data",
                data: form_data,
                headers: {
                    "X-CSRFToken": getCSRFToken(),

                },
                success: function (response) {
                    $("#profile_pic_img").attr("src", response);
                    console.log('Profile picture is changed successfully');
                },
                error: function (response) {
                    console.error('Error when profile picture change');
                }

            });

        }

    });


    /* popup -------------------------*/

    function removePupUp() {
        $('.alert').removeClass("show");
        $('.alert').addClass("hide");
    }

    $(".close-btn").click(removePupUp);

    var deleteDiv = null;

    $(".delete-trigger").click(function () {
        $("#delete-modal-container").addClass("show-modal")
        $("body").css("overflow", "hidden");
        deleteDiv = $(this).closest(".whole-plan");
    });

    $(".close-delete-modal").click(function () {
        $("#delete-modal-container").removeClass("show-modal");
        $("body").css("overflow", "auto");
        deleteDiv = null;
    })

    $("#delete-plan-btn").click(function () {

        if (deleteDiv == null) {
            return;
        }

        let params = {
            "plan_id": /\d*$/.exec($(deleteDiv).find("a").attr("href"))[0],
        }

        fetch("delete-plan", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCSRFToken()
            }, body: JSON.stringify(params)
        }).then(response => {
            if (response.status == 200) {
                $(deleteDiv).remove();
                $("#delete-modal-container").removeClass("show-modal");
                $("body").css("overflow", "auto");
            }
        })

    })

    var publishDiv = null;
    $(".window_trigger").click(function() {
        $("#publish-modal-container").addClass("show-modal")
        $("body").css("overflow", "hidden");
        if ($(this).closest(".my-whole-plan").find(".public-badge").length) {
            $("#public").prop("checked", true);
        } else {
            $("#public").prop("checked", false);
        }
        publishDiv = $(this).closest(".whole-plan");
    })

    $(".close-modal").click(function () {
        $("#publish-modal-container").removeClass("show-modal");
        $("body").css("overflow", "auto");
        publishDiv = null;
    })

    $("#public").click(function (event) {

        if (publishDiv == null) return;

        const params = {
            "state": $(this).prop("checked"),
            "plan_id": /\d*$/.exec($(publishDiv).find("a").attr("href"))[0]
        };

        $.ajax({
            url: "/publish-plan",
            type: "POST",
            async: false,
            data: JSON.stringify(params),
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCSRFToken()
            },
            success: function (response) {
                if (params.state) {
                    let elem = $("<span>Public</span>");
                    $(elem).addClass("badge").addClass("bg-primary").addClass("public-badge");
                    $(publishDiv).find(".plan-badges").append(elem);
                } else {
                    $(publishDiv).find(".public-badge").remove();
                }
            },
            error: function (response) {
                $(this).prop("checked", !params.state);
                event.preventDefault();

                $('.alert').addClass("show");
                $('.alert').removeClass("hide");
                $('.alert').addClass("showAlert");
                $('.alert').removeClass("success-col").removeClass("error-col").removeClass("warning-col");
                $(".my-bx").addClass("bxs-error-circle");
                $(".alert").addClass("error-col");

                if (response.status == 405) {
                    $('.msg').html("Error: You are not that type of user");
                } else if (response.status == 403) {
                    $('.msg').html("Error: This is not your plan you cannot change it");
                }

                setTimeout(removePupUp, 5000);
            }
        });
    });

    $("#send-plan-btn").click(function () {

        const params = {
            "user_sending": $("#sending-username").val(),
            "plan_id": /\d*$/.exec($(publishDiv).find("a").attr("href"))[0],
        }

        $.ajax({
            url: "send-plan",
            method: "POST",
            data: JSON.stringify(params),
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCSRFToken()
            },
            success: function (response) {
                $('.alert').addClass("show");
                $('.alert').removeClass("hide");
                $('.alert').addClass("showAlert");
                $('.alert').removeClass("success-col").removeClass("error-col").removeClass("warning-col");
                $(".my-bx").addClass("bxs-check-circle");
                $('.msg').html("SUCCESS: Plan is sent to user");
                $(".alert").addClass("success-col");
            },
            error: function (response) {
                $('.alert').addClass("show");
                $('.alert').removeClass("hide");
                $('.alert').addClass("showAlert");
                $('.alert').removeClass("success-col").removeClass("error-col").removeClass("warning-col");
                $(".my-bx").addClass("bxs-error-circle");
                $(".alert").addClass("error-col");

                if (response.status == 404) {
                    $('.msg').html("ERROR: User with that username does not exists");
                } else if (response.status == 403) {
                    $('.msg').html("ERROR: This is not your plan you cannot send it to anyone");
                }

                setTimeout(removePupUp, 5000);
            }

        });

    });

    function reloadNotifications() {
        let names = []
        $("#notifications-div button[aria-expanded=true]").each(function () {
            names.push($(this).attr("name"));
        });

        $.ajax({
            url: "get-notifications",
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCSRFToken()
            },
            data: JSON.stringify(names),
            success: function (response) {
                $("#notifications-div").html(response);
                addNotiListeners();
            }
        });

    }

    function addNotiListeners() {
        $(".noti-dismiss-btn").click(function () {

            let self = $(this);

            $.ajax({
                url: "dismiss-form",
                method: "POST",
                data: JSON.stringify({"form_id": $(this).attr("name")}),
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": getCSRFToken()
                },
                success: function (response) {
                    $(self).closest(".collapse").prev().remove();
                    $(self).closest(".collapse").remove();
                }

            })

        });

        $(".noti-ignore-btn").click(function() {

            let self = $(this);

            $.ajax({
                url: "delete-form",
                method: "POST",
                data: JSON.stringify({"id_form": $(this).attr("name")}),
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": getCSRFToken()
                },
                success: function (response) {
                    $(self).closest(".collapse").prev().remove();
                    $(self).closest(".collapse").remove();
                }
            });

        });
    }



    addNotiListeners();
    setInterval(reloadNotifications, 5000);
});