/*
Ana Vitkovic 0285/2021
*/

function changeValue(event) {
    let text = event.target.innerText;
    let span = document.getElementById("sort-text");
    span.innerText = text;
}

$(document).ready(function (){


     $("#nutri-search-button-ajax").click(function(){

         let params = {
            "search-input" : $("#search-nutri-input").val()
        }

         switch (document.getElementById("sort-text").innerText){

            case "Name A-Z":
                params["order"]="alphabeticalASC";
                break;
            case "Name Z-A":
                params["order"]="alphabeticalDESC";
                break;
            case "Grade 0-5":
                params["order"]="gradeASC";
                break;
            case "Grade 5-0":
                 params["order"]="gradeDESC";
                 break;
        };

         const queryString = new URLSearchParams(params);
         const url = `get-nutri-list?${queryString}`;

         // send request
        fetch(url).then(response => response.text().then(
                response =>$("#listedNutri").html(response)
            )
        );

     });

});