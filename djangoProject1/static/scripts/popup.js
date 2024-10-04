/*
Tijana Gasic 0247/2021
Natasa Spasic 0310/2021
*/
function showMessage(message) {
  if (message=="Didnt fill out every field") {
     $('.alert').addClass("show");
          $('.alert').removeClass("hide");
          $('.alert').removeClass("error-col");
          $('.alert').addClass("showAlert");
          $('.msg').html("Warning: Must fill out every field!");
          $(".alert").addClass("warning-col");

          setTimeout(function(){
              $('.alert').removeClass("show");
              $('.alert').addClass("hide");
          }, 5000);
  } else {
     $('.alert').addClass("show");
          $('.alert').removeClass("hide");
          $('.alert').removeClass("warning-col");
          $('.alert').addClass("showAlert");
          $('.msg').html("ERROR: False info data!");
          $(".alert").addClass("error-col");

          setTimeout(function(){
              $('.alert').removeClass("show");
              $('.alert').addClass("hide");
          }, 5000);
  }
}