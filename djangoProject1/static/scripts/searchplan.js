/*
Ana Vitkovic 0285/2021
*/
$(document).ready(function (){
    changeLabel();

    $("#plan-search-button-ajax").click(function(){

        let checkbox = document.getElementById('cb7');
        let includeDays=0;
        if(checkbox.checked){
            includeDays=1;
        }

        let params = {
            "search-input" : $("#search-plan-input").val(),
            "days": document.getElementById("num-of-days").innerText.replace(/\+/g, ''),
            "include-days": includeDays
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

        let filters=[];
        const checkboxes = document.querySelectorAll('input[type="checkbox"]:checked');
        const selectedLabels = [];
        if (checkboxes){
                checkboxes.forEach(checkbox => {
                    if(checkbox.id!="cb7"){
                         const label = checkbox.nextElementSibling;
                         selectedLabels.push(label.textContent);
                         filters=selectedLabels;
                    }
                });
        };
        params["filters"]=filters;

        const queryString = new URLSearchParams(params);
        const url = `get-plan-list?${queryString}`;

         // send request
        fetch(url).then(response => response.text().then(
                response =>$("#search-plans").html(response)
            )
        );
    });

});

    function searchPlan() {
        window.location.href = "planPage.html";
    }
    function changeLabel() {
        let dayValue = document.getElementById("num-of-days");
        let slider = document.getElementById("day-slider");

        dayValue.innerText = slider.value == 31 ? (slider.value - 1 + "+") : slider.value;
    }
    function changeValue(event) {
        let text = event.target.innerText;
        let span = document.getElementById("sort-text");
        span.innerText = text;
    }
    function toggleRange() {
        let checkbox = document.getElementById('cb7');
        let range = document.getElementById('day-slider');
        range.disabled = !checkbox.checked;
    }


