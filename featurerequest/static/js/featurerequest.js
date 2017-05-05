// Shows an alert box at the top of the page. 
//    type: 'fail' or 'success'
//    text: Text to be shown in the alert.
function showAlert(type, text) {
    $("#" + type + "Alert").text(text);
    $("#" + type + "Alert").fadeIn();
    $("#" + type + "Alert").delay(5000).fadeOut();
}

// To be reduced to knockout bindings soon(TM)!
function featureToggleDisplay(element) {
    var id = element.split("_")[1];
    var visible = $(element).is(":visible");
    $(".featureExpandable").hide();
    $(".featureExandableButton").removeClass("fa-caret-down");
    $(".featureExandableButton").addClass("fa-caret-right");
    if (!visible) {
        $("#featureExandableButton_" + id).removeClass("fa-caret-right");
        $("#featureExandableButton_" + id).addClass("fa-caret-down");
        // Get all data.
        var displayElement = $("#featureNoteDisplay_" + id);
        var firstHTML = '<div class="card"><div class="card-block"><p class="card-text m-0"><strong>';
        var secHTML = ': </strong>';
        var thirdHTML = '</p><p class="card-text"><small class="text-muted">';
        var lastHTML = '</small></p></div>';
        displayElement.html("");
        $.get("feature/" + id, {}, function (data) {
            if (data.hasOwnProperty('message')) {
                // Convert to a better error display...
                console.log("Sorry, you do not have permission to access this!");
            } else {
                // We've got the feature data, lets display it. :-)
                var created = new moment(data['feature']['created']).format("MMM D, YYYY [at] H:m A"); 
                var target = new moment(data['feature']['target_date']).format("MMM D, YYYY"); 
                if (target === "Invalid date") {
                    target = "";
                }
                var extraHTML = '<p class="card-text m-0"><strong>';
                var newHTML = firstHTML + "Description" + secHTML + data['feature']['description'] + '</p>' + extraHTML + 'Target Date' +
                    secHTML + target + '</p>' + extraHTML + 'Ticket URL' + secHTML + '<a href="' + data['feature']['ticket_url'] + '">' +
                    data['feature']['ticket_url'] + thirdHTML + created + lastHTML;
                displayElement.append(newHTML);
                $.get("featurenote/" + id, {}, function (data) {
                    if (data.hasOwnProperty('message')) {
                        // Convert to a better error display...
                        console.log("Sorry, you do not have permission to access this!");
                    } else {
                        data = data["feature_notes"];
                        for (var i in data) {
                            var created = new moment(data[i]['created']).format("MMM D, YYYY [at] H:m A"); 
                            var newHTML = firstHTML + data[i]['user'] + secHTML + data[i]['note'] + thirdHTML + created + lastHTML;
                            displayElement.append(newHTML);
                        }
                    }
                    displayElement.append('<div class="card" id="featureAddResponseDIV_' + id + '"><div class="card-block"><form id="featureAddResponse_' + id + '"><input type="hidden" name="feature_id" value="' + id + '"><div class="form-group"><label for="featureAddResponseText_' + id + '">Add Response:</label><textarea class="form-control" name="note" id="featureAddResponseText_' + id + '" rows="3"></textarea></div><button id="featureAddResponseButton_' + id + '" type="button" class="btn btn-primary">Submit</button></div></div>');
                    $("#featureAddResponseButton_" + id).on('click', function () {
                        var json_data = $("#featureAddResponse_" + id).serializeJSON();
                        var sendData = $.ajax({
                            url: "featurenote",
                            method: "POST",
                            data: json_data,
                            contentType: "application/json; charset=utf-8",
                            dataType: "json"
                        });
                        sendData.done(function (msg) {
                            data = msg['feature_note'];
                            var created = new moment(data['created']).format("MMM D, YYYY [at] H:m A");
                            var newHTML = firstHTML + data['user'] + secHTML + data['note'] + thirdHTML + created + lastHTML;
                            $(newHTML).insertBefore("#featureAddResponseDIV_" + id);
                        });
                    });
                    $(element).show();
                });
            }
        });
        
    }
}