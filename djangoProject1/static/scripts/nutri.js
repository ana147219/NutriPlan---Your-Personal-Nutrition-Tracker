/*
Natasa Spasic 0310/2021
*/
function gotoForm(nutritionistId) {
        let url = `/nutritionist/${nutritionistId}/order/`;
        console.log("Redirecting to:", url); // Log the URL
        window.location.href = url;
    }
