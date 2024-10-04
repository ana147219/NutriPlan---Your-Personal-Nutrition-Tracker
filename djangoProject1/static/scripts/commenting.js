
/*
Tijana Gasic 0247/2021
 */
function getCSRFToken() {
    /**
    Function returns csrf token from cookies
     */
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


function comm_success(data){
    /**
    function for creating comment
     */

    let com_wrapper=document.createElement("div");

    com_wrapper.classList.add("comment-wrapper");
    com_wrapper.classList.add("sb2");


    let c_u=document.createElement("div");
    c_u.classList.add("c-user");


    let pic=document.createElement("img");
    pic.classList.add("usr-img");
    pic.src=data['user_pic'];

    let u_name=document.createElement("span");
    u_name.classList.add("usr-name");
    u_name.textContent=data['username'];


    let u_text=document.createElement("p");
    u_text.classList.add("c-text");



    u_text.textContent=data['content'];


    c_u.appendChild(pic);
    c_u.appendChild(u_name);

    com_wrapper.appendChild(c_u);
    com_wrapper.appendChild(u_text);

    let container=document.getElementsByClassName("comments-wrp")[0];

    container.appendChild(com_wrapper);

    document.getElementsByClassName("cmnt-input")[0].value="";
}




function add_com_p(){

    let text_area_com=document.getElementsByClassName("cmnt-input")[0].value;

    if(text_area_com=="") return;


    $.ajax({
    /**
    send ajax request for posting comment
     */
    url: 'add_comment_plan',
    method: 'POST',
    dataType: "json",

    headers:{
        "Content-Type" : "application/json",
        "X-CSRFToken" : getCSRFToken()

    },
    data:JSON.stringify({"text":$('.cmnt-input').val()}),
    success:function (data) {

        comm_success(data)

    },
    error: function (response){
        console.error('Error while adding comment');
    }

});


}

function add_com_n(){


    let text_area_com=document.getElementsByClassName("cmnt-input")[0].value;

    if(text_area_com=="") return;


    $.ajax({
    /*
    send ajax request for posting comment
     */
    url: 'add_comment_nutri',
    method: 'POST',
    dataType: "json",

    headers:{
        "Content-Type" : "application/json",
        "X-CSRFToken" : getCSRFToken()

    },
    data:JSON.stringify({"text":$('.cmnt-input').val()}),
    success:function (data) {

        comm_success(data)

    },
    error: function (response){
        console.error('Error while adding comment');
    }

});

}







