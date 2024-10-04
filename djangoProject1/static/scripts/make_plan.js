import { generateHourArray, populateElement, centerScroll } from "./timeline.js";
import { settingButtons } from "./timeline.js";

let allDays = JSON.parse(document.getElementById("myData").textContent);
let lastDropTarget = null;
let foodTimeline;
let activeDay = "Day 1";

function createDay(textContent) {
    let newDay = {};

    for (let i = 0; i < 24; i++) {
        const hour = (i < 10 ? "0" : "") + i + ":00";
        newDay[hour] = [];
    }

    allDays[textContent] = newDay;
}

function restoreContent(event) {
    const text = event.currentTarget.textContent;
    $("#day-header").text(text);
    activeDay = text;
    foodTimeline = generateTimelineDragAndDrop(allDays[activeDay]);
    addListeners(foodTimeline);
}

export function generateTimelineDragAndDrop(food) {
    const hoursArray = generateHourArray();

    let foodTimeline = document.getElementById("timeline");
    foodTimeline.innerHTML = "";

    $.each(hoursArray, function(index, hour) {
        let foodTime = document.createElement("div");
        foodTime.classList.add("food-time");
        populateElement(foodTime, hour);
        foodTime.addEventListener("click", () => {
            centerScroll(foodTime, foodTimeline);
            //changeFood(img);
        });
        foodTimeline.appendChild(foodTime);

        let imgDiv = foodTime.querySelectorAll(".img-div")[0];

        $.each(food[hour], function(index, element) {
            let img = document.createElement("img");
            img.src = element.img;
            img.draggable = true;
            img.addEventListener("dragstart", removeFromPlan);
            img.addEventListener("allowDrop", allowDrop);
            img.addEventListener("dragend", dragEnd);

            imgDiv.appendChild(img);
        });
    });

    return foodTimeline;
}

export function addDay() {
    let newButton = $("<button></button>").addClass("btn").addClass("btn-primary").addClass("day-button");
    $(newButton).attr("data-bs-toggle", "button").attr("autocomplete", "off")
    const numberOfDays = $("#days").children(".day-button").length;

    let currentPos = $("#addDay").css("background-position-x");
    $(newButton).css("background-position-x", currentPos);
    currentPos = currentPos.match(/\d*(\.\d*)?/)[0];
    currentPos = parseFloat(currentPos) + (window.innerWidth > 768 ? 12.5 : 25);
    if (currentPos > 100) currentPos = 0;
    $("#addDay").css("background-position-x", currentPos + "%");

    const buttonText = `Day ${numberOfDays}`
    $(newButton).text(buttonText);
    $("#day-header").text(buttonText);
    $(newButton).click(restoreContent);
    createDay(buttonText);
    activeDay = buttonText;
    foodTimeline = generateTimelineDragAndDrop(allDays[buttonText]);
    addListeners(foodTimeline);

    $(newButton).insertBefore($("#addDay"));
    $("<span> </span>").insertBefore($("#addDay"));
}

function allowDrop(event) {
    event.preventDefault();
    lastDropTarget = event.target;
}

function drag(event) {
    if (event.target === event.currentTarget) {
        let img = event.target;
        let parentSearchItem = $(img).closest(".search-item");

        let transfer_data = {
            "img" : img.src,
            "amount" : $(parentSearchItem).find("input.form-control").val(),
            "food_id" : $(parentSearchItem).parent().attr("name")
        }
        event.dataTransfer.setData("application/json", JSON.stringify(transfer_data));
    } else {
        event.preventDefault();
    }
}

function drop(event) {
    event.preventDefault();
    let data = JSON.parse(event.dataTransfer.getData("application/json"));
    let hour = event.currentTarget.querySelectorAll(".timeline-legend")[0].innerText;
    allDays[activeDay][hour].push(data);
    let myDiv = event.currentTarget.querySelectorAll(".img-div")[0];
    let img = document.createElement("img");
    img.src = data.img;
    img.draggable = true;
    img.addEventListener("dragstart", removeFromPlan);
    img.addEventListener("allowDrop", allowDrop);
    img.addEventListener("dragend", dragEnd);
    myDiv.appendChild(img);
    lastDropTarget = null;
}

function addListeners(foodTimeline) {
    var children = foodTimeline.children;
    for (var i = 0; i < children.length; i++) {
        var logo = children[i];
        logo.addEventListener("dragover", allowDrop);
        logo.addEventListener("drop", drop);
    }
}

function dragEnd(event) {
    const trashCan = document.getElementById("trash-can");
    if (lastDropTarget == null || lastDropTarget == trashCan) {
        let hour = event.target.parentNode.parentNode.parentNode.querySelectorAll(".timeline-legend")[0].innerText;
        let index = allDays[activeDay][hour].findIndex(item => {
            let first = item.img.split("/").pop();
            let second = event.target.src.split("/").pop();
            return first == second;
        });

        allDays[activeDay][hour].splice(index, 1);
        event.target.parentNode.removeChild(event.target);
    }
}

function removeFromPlan(event) {
    if (event.target === event.currentTarget) {
        let img = event.target;
        let parentDiv = $(img).closest(".food-time");
        let data_array = allDays[activeDay][$(parentDiv).find(".timeline-legend").text()]

        let transfer_data;
        transfer_data = data_array[data_array.findIndex(item => {
            let first = item.img.split("/").pop();
            let second = img.src.split("/").pop();
            return first == second;
        })];

        event.dataTransfer.setData("application/json", JSON.stringify(transfer_data));
    } else {
        event.preventDefault();
    }
}

window.addDay = addDay;
window.drag = drag;
window.allowDrop = allowDrop;

function buttonGradientFix(step) {
    let currPos = 0;
    $("#days").children(".day-button").each(function() {
        $(this).css("background-position-x", currPos + "%");
        currPos += step;
        if (currPos > 100) {
            currPos = 0;
        }
    });
}

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

function reorderContent(event) {
    /**
     * It reorders main divs when resizing windows
     *
     */
    let column1 = document.getElementById("first-column");
    let column2 = document.getElementById("second-column");

    let days = document.getElementById("days-div");
    let timeline = document.getElementById("timeline-div");
    let footer = document.getElementById("footer-div");
    let searchFood = document.getElementById("search-food-div");

    column1.innerHTML = "";
    column2.innerHTML = "";

    column1.append(days);

    if (window.innerWidth < 768) {
        column1.append(searchFood);
        buttonGradientFix(25);
    } else {
        column2.append(searchFood);
        buttonGradientFix(12.5);
    }

    column1.append(timeline);
    column1.append(footer)
}

function removePupUp() {
    $('.alert').removeClass("show");
    $('.alert').addClass("hide");
}

$(document).ready(function() {
    let lastWindowWidth = window.innerWidth;

    $(window).resize(function () {
        if (Math.abs(window.innerWidth - lastWindowWidth) > 0) {
            lastWindowWidth = window.innerWidth;
            reorderContent();
        }
    })

    settingButtons();
    $(".day-button").click(restoreContent);
    $("#addDay").unbind();
    $("#addDay").click(addDay);
    foodTimeline = generateTimelineDragAndDrop(allDays[activeDay]);
    reorderContent();
    addListeners(foodTimeline);

    $(".form-check-input").prop("checked", false);
    // function that will remain only one checkbox active
    var current = null;
    $(".form-check-input").change(function () {
        if (current == $(this).attr("name")) {
            current = null;
            return;
        }

        $(".form-check-input").prop("checked", false);
        $(this).prop("checked", true);


        current = $(this).attr("name");
    })

    // when user click search button sends ajax request to get data
    $("#food-search-button-ajax").click(function () {
        // first make loading spinner
        let spinner = $("<div></div>").addClass("d-flex").addClass("justify-content-center")
        $(spinner).html($("<div></div>").addClass("spinner-border").addClass("m-5"))
        $("#search-food").html(spinner);

        // take user parameters
        let params = {
            "food-name" : $("#food-search-input").val(),
        }
        if (current) {
            params["food-type"] = current;
        }
        const queryString = new URLSearchParams(params);

        const url = `get-food-list?${queryString}`;

        // send request
        fetch(url).then(response => response.text().then(
                response =>$("#search-food").html(response)
            )
        );
    });

    $('.close-btn').click(removePupUp);

    // sending ajax request when we want to save plan
    $("#save-button").click(function () {

        const params = {
            "days": allDays,
            "name": $("#input-plan-name").val(),
            "tags": $(".btn-check:checked").map(function() {
                        return $(this).attr("name");
                    }).get()
        }

        fetch("save-plan", {
            method: "POST",
            headers: {
                "Content-Type" : "application/json",
                "X-CSRFToken" : getCSRFToken()
            },
            body: JSON.stringify(params),
        }).then(
            response => {
                $('.alert').addClass("show");
                $('.alert').removeClass("hide");
                $('.alert').addClass("showAlert");
                $('.alert').removeClass("success-col").removeClass("error-col").removeClass("warning-col");
                $(".my-bx").removeClass("bxs-error-circle").removeClass("bxs-check-circle");

                if (response.status == 201) {
                    $(".my-bx").addClass("bxs-check-circle");
                    $('.msg').html("Success: Plan is successfully saved!");
                    $(".alert").addClass("success-col");
                } else if (response.status == 403) {
                    $(".my-bx").addClass("bxs-error-circle");
                    $('.msg').html("Error: You are not owner of this plan");
                    $(".alert").addClass("error-col");
                }

                setTimeout(removePupUp,5000);
            }
        )
    })

    $("#begin-button").click(function() {
        fetch("begin-plan", {
            method: "POST",
            headers: {
                "X-CSRFToken" : getCSRFToken()
            }
        }).then(response => {
            $('.alert').removeClass("success-col").removeClass("error-col").removeClass("warning-col");
            $(".my-bx").removeClass("bxs-error-circle").removeClass("bxs-check-circle");
            $('.alert').addClass("show");
            $('.alert').removeClass("hide");
            $('.alert').addClass("showAlert");

            if (response.status == 201) {
                $(".my-bx").addClass("bxs-check-circle");
                $('.msg').html("Success: You can start your plan now");
                $(".alert").addClass("success-col");
            } else if (response.status == 400) {
                $(".my-bx").addClass("bxs-error-circle");
                $('.msg').html("Warning: You are already on a plan");
                $(".alert").addClass("warning-col");
            }

            setTimeout(removePupUp,5000);
        })
    })

});