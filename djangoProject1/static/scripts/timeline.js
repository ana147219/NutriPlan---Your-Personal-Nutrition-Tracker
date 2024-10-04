let current_meal = null;

export function generateHourArray() {
    const hoursArray = [];

    for (let i = 0; i < 24; i++) {
        const hour = (i < 10 ? "0" : "") + i + ":00";
        hoursArray.push(hour);
    }

    return hoursArray;
}

function makeLegend(hour) {
    let legend = document.createElement("div");
    legend.classList.add("timeline-legend");
    legend.innerHTML = hour;
    return legend;
}

function makeGrid() {
    let grid = document.createElement("div");
    grid.classList.add("grid-background");
    return grid;
}

function generateImageDiv(id) {
    let imgDiv = document.createElement("div");
    imgDiv.classList.add("img-div");

    return imgDiv;
}

function makeInfo(hour) {
    let info = document.createElement("div");
    info.classList.add("info");
    info.appendChild(makeGrid());
    info.appendChild(generateImageDiv());

    return info;
}

export function populateElement(foodTime, hour) {
    foodTime.appendChild(makeInfo(hour));
    foodTime.appendChild(makeLegend(hour));
}

export function generateFoodTimeline() {
    const hoursArray = generateHourArray();

    let foodTimeline = document.getElementById("timeline");

    hoursArray.forEach((hour) => {
        let foodTime = document.createElement("div");
        foodTime.classList.add("food-time");

        populateElement(foodTime, hour);

        foodTime.addEventListener("click", () => {
            centerScroll(foodTime, foodTimeline);
        });

        foodTimeline.appendChild(foodTime);
    });
}
export function centerScroll(item, container) {
    const itemRect = item.getBoundingClientRect();
    const containerWidth = container.offsetWidth;
    const shiftAmount = itemRect.left - containerWidth / 2;

    container.scrollBy({
        left: shiftAmount,
        behavior: "smooth",
    });
}

export function food_finished(event) {
    if (current_meal) {
        current_meal.classList.add("finished");
        console.log(current_meal);
    }
}

export function settingButtons() {
    let buttonLeft = document.getElementById("left-button");
    let buttonRight = document.getElementById("right-button");
    let container = document.getElementById("timeline");

    buttonLeft.addEventListener("click", function () {
        container.scrollBy({
            left: -container.offsetWidth * 0.1,
            behavior: "smooth",
        });
    });

    buttonRight.addEventListener("click", function () {
        container.scrollBy({
            left: container.offsetWidth * 0.1,
            behavior: "smooth",
        });
    });
}

var timeline = document.getElementById("timeline");

var startTouchX, lastTouchX, totalScrollX = 0;
var isScrolling = false;

timeline.addEventListener("touchstart", function(event) {
    startTouchX = event.touches[0].clientX;
    lastTouchX = startTouchX;
    totalScrollX = 0;
    isScrolling = true;
});

timeline.addEventListener("touchmove", function(event) {
    if (!isScrolling) return;
    
    var currentTouchX = event.touches[0].clientX;
    var diffX = currentTouchX - lastTouchX;
    lastTouchX = currentTouchX;
    totalScrollX += diffX;

    timeline.scrollLeft -= diffX;
});

timeline.addEventListener("touchend", function(event) {
    isScrolling = false;

    var momentum = totalScrollX * 0.3;
    timeline.scrollTo({
        left: timeline.scrollLeft - momentum,
        behavior: "smooth"
    });
});
