var activeCell = null;

function myDate(day, month, year) {
    /**
    Class represenst current date in calendar
     */
    this.cell = document.createElement("li");
    this.day = day;
    this.month = month;
    this.year = year;
    this.cell.innerHTML = day;
    this.cell.addEventListener("click", () => {this.activateDay(true)});
}

myDate.prototype.activateDay = function(isClick) {
    /**
    Change day highlight and takes from database timeline of that day
     */
    if (this.day == "&nbsp") return;
    if (activeCell) {
        activeCell.deactivateDay();
    }
    this.cell.innerHTML = "";
    let span = document.createElement("span");
    span.classList.add("active");
    span.innerHTML = this.day;
    this.cell.appendChild(span);
    activeCell = this;
    if (isClick) {
        this.getTimeline();
    }
};

myDate.prototype.getTimeline = function() {
    /**
    Sends ajax request that will return timeline for specified date
    and loads that html in page
     */

    const params = {
        "year": this.year,
        "month": this.month + 1,
        "day": this.day
    }

    const queryString = new URLSearchParams(params);

    const url = `date-food-timeline?${queryString}`;

    fetch(url).then(response => response.text().then(
        response => {
            $("#timeline").html(response);
            timelineAddListeners();
        }
    ));

}

myDate.prototype.deactivateDay = function() {
    this.cell.innerHTML = "";
    this.cell.innerHTML = this.day;
};

function generateMonthHeader(month, year) {
    /**
    Generate calendar header that contains month and year
    through javascript based on current month and year
     */
    var months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];

    var monthHeader = document.createElement("div");
    monthHeader.classList.add("month");
    var uList = document.createElement("ul");
    var iList = document.createElement("li");
    monthHeader.appendChild(uList);
    uList.appendChild(iList);
    var monthName = document.createElement("div");
    var yearDisplay = document.createElement("div");
    iList.appendChild(monthName);
    iList.append(yearDisplay);
    monthName.innerHTML = months[month];
    yearDisplay.innerHTML = year;

    return monthHeader;
}
function generateWeekdays() {
    /**
    Generate weekdays header
     */
    var weekdays = ["Su", "Mo", "Tu", "We", "Th", "Fr", "Sa"];

    var uList = document.createElement("ul");
    uList.classList.add("weekdays");

    for (var i = 0; i < weekdays.length; i++) {
        var lItem = document.createElement("li");
        lItem.innerText = weekdays[i];
        uList.appendChild(lItem);
    }

    return uList;
}
function generateCalendarDays(month, year) {
    /**
    based on month and year counts days and put them in calendar so weekdays and days match
     */

    var today = new Date();
    var daysInMonth = new Date(year, month + 1, 0).getDate();
    var firstDayOfMonth = new Date(year, month, 1).getDay();

    var calendarBody = document.createElement("ul");
    calendarBody.classList.add("days");

    for (var i = 0; i < firstDayOfMonth; i++) {
        var cell = new myDate("&nbsp");
        calendarBody.appendChild(cell.cell);
    }

    for (var i = 1; i <= daysInMonth; i++) {
        var cell = new myDate(i, month, year);
        if (activeCell == null && i == today.getDate() && month == today.getMonth() && year == today.getFullYear()) {
            cell.activateDay(false);
        } else if (activeCell != null && i == activeCell.day && month == activeCell.month && year == activeCell.year) {
            cell.activateDay(false);
        }
        calendarBody.appendChild(cell.cell);
    }

    return calendarBody;
}

function getCSRFToken() {
    /**
    returns csrf token from cookies and which will be used for ajax request
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

export function timelineAddListeners() {
    $(".food-time").click(function (event) {
        /**
        add scroll listener for food time so every time somebody
        click part with hour it comes to center
         */

        const itemRect = $(this).get(0).getBoundingClientRect();
        const containerWidth = $("#timeline").get(0).offsetWidth;
        const shiftAmount = itemRect.left - containerWidth / 2;

        $("#timeline").get(0).scrollBy({
            left: shiftAmount,
            behavior: "smooth",
        });

    })

    function make_circle(progress_value) {
        /**
        Function is used when reloading circle or
        loading page, it accepts progress and loads circle
        */
        let options = {
        startAngle: -1.55,
        size: 150,
        value: progress_value,
        fill: { gradient: ["#00aaff", "#a445b2"] },
        };

        $(".circle .bar")
            .circleProgress(options)
            .on("circle-animation-progress", function (event, progress, stepValue) {
            var val;
            if(Number.isInteger(stepValue)){
                stepValue *= 100;
                val=stepValue.toString();
            }
            else{
                stepValue *= 100;
                val=stepValue.toFixed(2);
                val=parseFloat(val).toString()
            }

            $(this).parent().find("span").text(val + "%");
            });
    }

    $(".food-time img").click(function() {
        /**
        When user press image ajax request will be sent
        and information about meal will be embedded to
        meal status div
         */

        const params = {
            "id": $(this).data("id")
        }

        const queryString = new URLSearchParams(params);

        const url = `get-meal-info?${queryString}`;

        fetch(url).then(response => response.text().then(
            response => {
                $("#meal-div").html(response);

                $("#change-meal-button").click(function() {
                    /**
                    If user wants to finish his meal he sends ajax request
                    and if the time for that meal is now, meal will be finished
                    if not pop up message is displayed
                     */

                    $.ajax({
                        url: "finish-meal",
                        method: "POST",
                        dataType: "json",
                        headers: {
                            "Content-Type" : "application/json",
                            "X-CSRFToken" : getCSRFToken()
                        },
                        data: JSON.stringify({"id": $(this).attr("name")}),
                        success: function (response) {
                            $("#timeline").html(response["timeline"]);
                            make_circle(response["progress"]);
                            timelineAddListeners();
                        },
                        error: function (response) {
                            if (response.status == 425) {
                                $(".alert").addClass("show");
                                $(".alert").removeClass("hide");
                                $('.alert').addClass("showAlert");

                                setTimeout(function () {
                                    $(".alert").removeClass("show");
                                    $(".alert").addClass("hide");
                                }, 5000)
                            }
                        }
                    })

                })
            }
        ))
    });
}
export function generateCalendar(containerId, month, year) {
    /**
    It generates our calendar
     */
    const container = document.getElementById(containerId);
    container.innerHTML = "";

    var myItem = document.createElement("div");
    myItem.appendChild(generateMonthHeader(month, year));
    myItem.appendChild(generateWeekdays());
    myItem.appendChild(generateCalendarDays(month, year));

    container.appendChild(myItem);
}

function subMonth(date) {
    /**
    Takes date and returns date which is one month earlier
     */
    let newDate = new Date(date);
    newDate.setMonth(date.getMonth() - 1);
    return newDate;
}

function addMonth(date) {
    /**
    Takes date and returns date which is one month later
     */
    let newDate = new Date(date);
    newDate.setMonth(date.getMonth() + 1);
    return newDate;
}
export function generateCarousel() {
    /**
    Making our calendar function to slide between months
     */
    const today = new Date();
    let today0 = subMonth(today);
    let today1 = new Date(today);
    let today2 = addMonth(today);

    generateCalendar("calendar0", today0.getMonth(), today0.getFullYear());
    generateCalendar("calendar1", today1.getMonth(), today1.getFullYear());
    generateCalendar("calendar2", today2.getMonth(), today2.getFullYear());

    document.getElementById("myCarousel").addEventListener("slid.bs.carousel", function () {
        const activeIndex = Array.from(document.querySelectorAll(".carousel-item")).findIndex((item) => item.classList.contains("active"));

        switch (activeIndex) {
            case 0:
                today1 = addMonth(today0);
                today2 = subMonth(today0);
                break;
            case 1:
                today0 = subMonth(today1);
                today2 = addMonth(today1);
                break;
            case 2:
                today0 = addMonth(today2);
                today1 = subMonth(today2);
                break;
        }

        generateCalendar("calendar0", today0.getMonth(), today0.getFullYear());
        generateCalendar("calendar1", today1.getMonth(), today1.getFullYear());
        generateCalendar("calendar2", today2.getMonth(), today2.getFullYear());
    });

    document.getElementById("btn-left").addEventListener("click", function (event) {
        event.preventDefault();
        let carousel = new bootstrap.Carousel(document.getElementById("myCarousel"));
        carousel.prev();
    });

    document.getElementById("btn-right").addEventListener("click", function (event) {
        event.preventDefault();
        let carousel = new bootstrap.Carousel(document.getElementById("myCarousel"));
        carousel.next();
    });
}
