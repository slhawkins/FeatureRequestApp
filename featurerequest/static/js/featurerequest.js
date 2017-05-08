// Shows an alert box at the top of the page.
//    type: 'fail' or 'success'
//    text: Text to be shown in the alert.
function showAlert(type, text) {
    "use strict";
    $("#" + type + "Alert").text(text);
    $("#" + type + "Alert").fadeIn();
    $("#" + type + "Alert").delay(5000).fadeOut();
}