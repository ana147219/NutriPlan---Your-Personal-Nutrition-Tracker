import { generateCarousel, timelineAddListeners } from "./calendar.js";
import { generateFoodTimeline, settingButtons, food_finished } from "./timeline.js";

generateCarousel();
settingButtons();

/* circle progress bar */

let options = {
    startAngle: -1.55,
    size: 150,
    value: document.getElementById("myData").textContent,
    /*fill: {gradient: ['#a445b2', '#fa4299']}*/

    fill: { gradient: ["#00aaff", "#a445b2"] },
};

$(".circle .bar")
    .circleProgress(options)
    .on("circle-animation-progress", function (event, progress, stepValue) {
        /*
        loads progress slider based on data
         */
        var val;
        if(Number.isInteger(stepValue)){
            stepValue*=100
            val=stepValue.toString();
        }
        else{
            stepValue*=100
            val=stepValue.toFixed(2);
            val=parseFloat(val).toString()
        }
        $(this)
            .parent()
            .find("span")
            .text(val + "%");
    });

function reorderContent(event) {
    /*
    function used when resizing window so reaorder our content
     */
    let column1 = document.getElementById("first-column");
    let column2 = document.getElementById("second-column");

    let calendar = document.getElementById("calendar-div");
    let timeline = document.getElementById("timeline-div");
    let progress = document.getElementById("progress-div");
    let meal = document.getElementById("meal-div");

    column1.innerHTML = "";
    column2.innerHTML = "";

    if (window.innerWidth < 768) {
        column1.append(progress);
        column1.append(calendar);
        column1.append(timeline);
        column2.append(meal);
    } else {
        column1.append(calendar);
        column1.append(timeline);
        column2.append(progress);
        column2.append(meal);
    }
}

let lastWindowWidth = window.innerWidth;
let lastWindowHeight = window.innerHeight;

window.addEventListener("load", reorderContent);
window.addEventListener("resize", () => {

    if (Math.abs(window.innerWidth - lastWindowWidth) > 0) {
        lastWindowWidth = window.innerWidth;
        reorderContent();
    }
});

$(document).ready(function() {

    timelineAddListeners();

    $("#give-up-button").click(function() {
        /*
        opens modal asking user is he sure that he want to give up
         */
        $(document.body).css("overflow","hidden");
        $("#modal-container").addClass("show-modal");
    })

    $(".close-modal").click(function() {
        /*
        closing modal if user want to continue with plan
         */
        $(document.body).css("overflow", "auto");
        $("#modal-container").removeClass("show-modal");
    })

    $(".close-btn").click(function() {
        /*
        Closes pop up (when user is not ready to eat meal
         */
       $(".alert").removeClass("show");
       $(".alert").addClass("hide");
    });
})
