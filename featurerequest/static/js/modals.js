// Modal Validations
$("#addFeatureForm").validate({
    rules: {
        addFeaturePriority: {
            min: 1
        }
    }
});
$("#editFeatureForm").validate({
    rules: {
        editFeaturePriority: {
            min: 1
        }
    }
});
$("#addClientForm").validate({
    rules: {
        addClientPhone: {
            phoneUS: true
        }
    }
});
$("#editClientForm").validate({
    rules: {
        editClientPhone: {
            required: true,
            phoneUS: true
        }
    }
});

$("#addProductForm").validate();
$("#editProductForm").validate();
$("#addUserForm").validate();
$("#editUserForm").validate();


// Sends a POST to the server with the form data.
//     data_type: 'feature', 'client', 'product', or 'user'
//     show_value: Value from the response that is displayed in the success message.
function addDataForm(data_type, show_value) {
    "use strict";
    var type_upper = data_type.charAt(0).toUpperCase() + data_type.slice(1);
    var json_data = $("#add" + type_upper + "Form").serializeJSON();
    if ($("#add" + type_upper + "Form").valid()) {
        var sendData = $.ajax({
            url: data_type,
            method: "POST",
            data: json_data,
            contentType: "application/json; charset=utf-8",
            dataType: "json"
        });
        $("#add" + type_upper + "Modal").modal("hide");
        $("#add" + type_upper + "Form").trigger("reset");
        if (data_type === "feature") {
            $("addFeatureDate").datepicker("clearDates");
        }
        sendData.done(function (msg) {
            showAlert("success", "Added " + msg[data_type][show_value] + " to the database.");
            featureRequestViewModel.updateData(data_type);
        });
        sendData.fail(function (response) {
            showAlert("fail", "Error: " + response.responseJSON.message);
        });
    }
}

// Sends a PUT to the server with the form data.
//     data_type: 'feature', 'client', 'product', or 'user'
//     show_value: Value from the response that is displayed in the success message.
function editDataForm(data_type, show_value) {
    "use strict";
    var type_upper = data_type.charAt(0).toUpperCase() + data_type.slice(1);
    var json_data = $("#edit" + type_upper + "Form").serializeJSON();
    if ($("#edit" + type_upper + "Form").valid()) {
        var sendData = $.ajax({
            url: data_type + "/" + $("#edit" + type_upper + "ID").val(),
            method: "PUT",
            data: json_data,
            contentType: "application/json; charset=utf-8",
            dataType: "json"
        });
        $("#edit" + type_upper + "Modal").modal("hide");
        $("#edit" + type_upper + "Form").trigger("reset");
        sendData.done(function (msg) {
            showAlert("success", "Updated " + msg[data_type][show_value] + ".");
            featureRequestViewModel.updateData(data_type);
        });
        sendData.fail(function (response) {
            if (response === "undefined") {
                showAlert("fail", "Unknown server-side error occured. :-(");
            } else {
                showAlert("fail", "Error: " + response.responseJSON.message);
            }
        });
    }
}

// Sends a DELETE to the server with the id of the item to be deleted.
//     data_type: 'feature', 'client', 'product', or 'user'
//     show_value: Value from the response that is displayed in the success message.
function deleteDataForm(data_type, show_value) {
    "use strict";
    var type_upper = data_type.charAt(0).toUpperCase() + data_type.slice(1);
    var sendData = $.ajax({
        url: data_type + "/" + $("#delete" + type_upper + "ID").val(),
        method: "DELETE",
        dataType: "json"
    });
    $("#delete" + type_upper + "Modal").modal("hide");
    sendData.done(function (msg) {
        if (data_type === "client" || data_type === "feature") {
            showAlert("success", "Deleted " + msg[data_type][show_value] + ".");
        } else {
            showAlert("success", "Deactivated " + msg[data_type][show_value] + ".");
        }
        featureRequestViewModel.updateData(data_type);
        if (data_type === "client") {
            featureRequestViewModel.updateData("feature");
        }
    });
    sendData.fail(function (response) {
        if (response === "undefined") {
            showAlert("fail", "Unknown server-side error occured. :-(");
        } else {
            showAlert("fail", "Error: " + response.responseJSON.message);
        }
    });
}

// Bug workaround
// http://stackoverflow.com/questions/30113228/why-does-bootstrap-datepicker-trigger-show-bs-modal-when-it-is-displayed
$("#editFeatureModal .datepicker").on("show", function (e) {
    "use strict";
    e.preventDefault();
    e.stopPropagation();
}).on("hide", function (e) {
    "use strict";
    e.preventDefault();
    e.stopPropagation();
});

// Bug workaround
// http://stackoverflow.com/questions/30113228/why-does-bootstrap-datepicker-trigger-show-bs-modal-when-it-is-displayed
$("#addFeatureModal .datepicker").on("show", function (e) {
    "use strict";
    e.preventDefault();
    e.stopPropagation();
}).on("hide", function (e) {
    "use strict";
    e.preventDefault();
    e.stopPropagation();
});
$("#editFeatureModal").on("show.bs.modal", function (event) {
    "use strict";
    var button = $(event.relatedTarget);
    var id = button.data("id");
    var modal = $(this);
    // Thanks guys!
    // http://stackoverflow.com/questions/7364150/find-object-by-id-in-an-array-of-javascript-objects
    var result = $.grep(featureRequestViewModel.featureData(), function (e) {
        return e.id === id;
    });
    if (result.length !== 1) {
        console.log("Ooops");
        return;
        // Need to put an error message here.
    }
    var data = result[0];
    modal.find(".modal-title").text("Edit Feature: " + data.title);
    modal.find("#editFeatureID").val(data.id);
    modal.find("#editFeatureTitle").val(data.title);
    modal.find("#editFeatureDescription").val(data.description);
    modal.find("#editFeatureClient option").text(data.client);
    modal.find("#editFeatureClient option").val(data.client_id);
    modal.find("#editFeatureClientHidden").val(data.client_id);
    modal.find("#editFeaturePriority").val(data.priority);
    if (data.target_date !== "" && data.target_date !== null) {
        // setUTCDate was used here to prevent it from trying to change the date based on local timezone.
        modal.find(".datepicker").datepicker("setUTCDate", new Date(data.target_date));
    } else {
        modal.find(".datepicker").datepicker("update", "");
    }
    modal.find("#editFeatureURL").val(data.ticket_url);
    modal.find("#editFeatureProduct").val(data.product_id);
    // Reset product options. We want a feature with a disabled product to still be able to save with it.
    $("#editFeatureModal").find("#editFeatureProduct > option").each(function () {
        var element = $(this);
        // Reset the settings...
        element.show();
        if (element.data("active") !== "Yes") {
            element.attr("disabled", "disabled");
        }
        // Check if we should hide it or enable it.
        if (element.attr("disabled") === "disabled" && this.value !== data.product_id) {
            element.hide();
        } else {
            element.attr("disabled", false);
        }
    });
});


$("#editFeatureModal").on("hide.bs.modal", function () {
    "use strict";
    $(this).find(".datepicker").datepicker("update", "");
});

$("#addFeatureModal").on("hide.bs.modal", function () {
    "use strict";
    $(this).find(".datepicker").datepicker("update", "");
});

$("#editClientModal").on("show.bs.modal", function (event) {
    "use strict";
    var button = $(event.relatedTarget);
    var id = button.data("id");
    var modal = $(this);
    // Thanks guys!
    // http://stackoverflow.com/questions/7364150/find-object-by-id-in-an-array-of-javascript-objects
    var result = $.grep(featureRequestViewModel.clientData(), function (e) {
        return e.id === id;
    });
    if (result.length !== 1) {
        showAlert("fail", "Error: Could not find the given Client");
    }
    var data = result[0];
    modal.find(".modal-title").text("Edit Client: " + data.name);
    modal.find("#editClientID").val(data.id);
    modal.find("#editClientName").val(data.name);
    modal.find("#editClientPOC").val(data.poc);
    modal.find("#editClientEmail").val(data.email);
    modal.find("#editClientPhone").val(data.phone);
});

$("#editProductModal").on("show.bs.modal", function (event) {
    "use strict";
    var button = $(event.relatedTarget);
    var id = button.data("id");
    var modal = $(this);
    // Thanks guys!
    // http://stackoverflow.com/questions/7364150/find-object-by-id-in-an-array-of-javascript-objects
    var result = $.grep(featureRequestViewModel.productData(), function (e) {
        return e.id === id;
    });
    if (result.length !== 1) {
        showAlert("fail", "Error: Could not find the given Product");
    }
    var data = result[0];
    modal.find(".modal-title").text("Edit Product: " + data.name);
    modal.find("#editProductID").val(data.id);
    modal.find("#editProductName").val(data.name);
    modal.find("#editProductDescription").val(data.description);
    if (data.active === "Yes") {
        modal.find("#editProductActive").val("1");
    } else {
        modal.find("#editProductActive").val("");
    }
});

$("#editUserModal").on("show.bs.modal", function (event) {
    "use strict";
    var button = $(event.relatedTarget);
    var id = button.data("id");
    var modal = $(this);
    // Thanks guys!
    // http://stackoverflow.com/questions/7364150/find-object-by-id-in-an-array-of-javascript-objects
    var result = $.grep(featureRequestViewModel.userData(), function (e) {
        return e.id === id;
    });
    if (result.length !== 1) {
        showAlert("fail", "Error: Could not find the given User");
    }
    var data = result[0];
    modal.find(".modal-title").text("Edit User: " + data.username);
    modal.find("#editUserID").val(data.id);
    modal.find("#editUserName").val(data.username);
    modal.find("#editUserRole").val(data.role);
});

$("#deleteFeatureModal").on("show.bs.modal", function (event) {
    "use strict";
    var button = $(event.relatedTarget);
    var id = button.data("id");
    var modal = $(this);
    // Thanks guys!
    // http://stackoverflow.com/questions/7364150/find-object-by-id-in-an-array-of-javascript-objects
    var result = $.grep(featureRequestViewModel.featureData(), function (e) {
        return e.id === id;
    });
    if (result.length !== 1) {
        showAlert("fail", "Error: Could not find the given Feature");
    }
    var data = result[0];
    modal.find(".modal-title").text("Delete Feature: " + data.title);
    modal.find("#deleteFeatureText").text("Are you sure you want to delete " + data.title + "?");
    modal.find("#deleteFeatureID").val(id);
});

$("#deleteClientModal").on("show.bs.modal", function (event) {
    "use strict";
    var button = $(event.relatedTarget);
    var id = button.data("id");
    var modal = $(this);
    // Thanks guys!
    // http://stackoverflow.com/questions/7364150/find-object-by-id-in-an-array-of-javascript-objects
    var result = $.grep(featureRequestViewModel.clientData(), function (e) {
        return e.id === id;
    });
    if (result.length !== 1) {
        showAlert("fail", "Error: Could not find the given Client");
    }
    var data = result[0];
    modal.find(".modal-title").text("Delete Client: " + data.name);
    modal.find("#deleteClientText").text("Are you sure you want to delete " + data.name + " and all data associated with that client?");
    modal.find("#deleteClientID").val(id);
});

$("#deleteProductModal").on("show.bs.modal", function (event) {
    "use strict";
    var button = $(event.relatedTarget);
    var id = button.data("id");
    var modal = $(this);
    // Thanks guys!
    // http://stackoverflow.com/questions/7364150/find-object-by-id-in-an-array-of-javascript-objects
    var result = $.grep(featureRequestViewModel.productData(), function (e) {
        return e.id === id;
    });
    if (result.length !== 1) {
        showAlert("fail", "Error: Could not find the given Product");
    }
    var data = result[0];
    modal.find(".modal-title").text("Deactivate Product Area: " + data.name);
    modal.find("#deleteProductText").text("Are you sure you want to deactivate the product area " + data.name + "? Current features with this product area will not be changed.");
    modal.find("#deleteProductID").val(id);
});

$("#deleteUserModal").on("show.bs.modal", function (event) {
    "use strict";
    var button = $(event.relatedTarget);
    var id = button.data("id");
    var modal = $(this);
    // Thanks guys!
    // http://stackoverflow.com/questions/7364150/find-object-by-id-in-an-array-of-javascript-objects
    var result = $.grep(featureRequestViewModel.userData(), function (e) {
        return e.id === id;
    });
    if (result.length !== 1) {
        showAlert("fail", "Error: Could not find the given User");
    }
    var data = result[0];
    modal.find(".modal-title").text("Deactivate User: " + data.username);
    modal.find("#deleteUserText").text("Are you sure you want to deactivate " + data.username + "?");
    modal.find("#deleteUserID").val(id);
});