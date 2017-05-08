function FeatureRequestViewModel() {
    var self = this;
    // Setup data observables. They have the following types:
    // _____Watch    : Watch variables are used to update the data table when
    //                 either its column order or data has changed. 
    // _____Data     : Data retrieved from the API
    // _____Columns  : Column order, could be easily changed for the user.
    // _____ColumnMap: Contains a map from the field names retrieved via the API
    //                 to column titles.
    // TODO: Subscribers can likely be removed now, just need to update the HTML.
    // Features
    self.featureWatch = ko.observable(1);
    self.featureData = ko.observableArray([]);
    self.featureColumns = ko.observable(featureColumnsOrder);
    self.featureColumnMap = featureColumnsMap;
    self.featureColumns.subscribe(function () { self.featureWatch(1 + self.featureWatch()); });
    self.featureDiscussionData = ko.observable({});
    self.featurePriorityMin = ko.observable(1);
    self.featurePriorityMax = ko.observable(10);
    self.featurePriorityMin.subscribe(function () {
        if (self.sliderInit) {
            $("#slider-range").slider("option", "min", self.featurePriorityMin());
            $("#slider-range").slider("option", "value", [self.featurePriorityMin(), self.featurePriorityMax()]);
            $("#sliderAmount").text("Priority Range: " + $("#slider-range").slider("values", 0) + " - " + $("#slider-range").slider("values", 1));
        }
    });
    self.featurePriorityMax.subscribe(function () {
        if (self.sliderInit) {
            $("#slider-range").slider("option", "max", self.featurePriorityMax());
            $("#slider-range").slider("option", "value", [self.featurePriorityMin(), self.featurePriorityMax()]);
            $("#sliderAmount").text("Priority Range: " + $("#slider-range").slider("values", 0) + " - " + $("#slider-range").slider("values", 1));
        }
    });
    // Clients
    self.clientWatch = ko.observable(1);
    self.clientData = ko.observableArray([]);
    self.clientColumns = ko.observable(clientColumnsOrder);
    self.clientColumnMap = clientColumnsMap;
    self.clientColumns.subscribe(function () { self.clientWatch(1 + self.clientWatch()); });
    self.clientNamesOrdered = ko.pureComputed(function () {
        // Quick sort
        // Might be a hack - but we need this to break down the multiselect.
        //$('#addFeatureClient').multiselect('destroy');
        //$('#addFeatureClient').find('option').remove();
        // http://stackoverflow.com/questions/1129216/sort-array-of-objects-by-string-property-value-in-javascript
        names = self.clientData()
        names.sort(function (a, b) { return (a.name > b.name) ? 1 : ((b.name > a.name) ? -1 : 0); });
        return names;
    });
    // Products
    self.productWatch = ko.observable(1);
    self.productData = ko.observableArray([]);
    self.productColumns = ko.observable(productColumnsOrder);
    self.productColumnMap = productColumnsMap;
    self.productColumns.subscribe(function () { self.productWatch(1 + self.productWatch()); });
    self.productNamesOrdered = ko.pureComputed(function () {
        // Quick sort
        // http://stackoverflow.com/questions/1129216/sort-array-of-objects-by-string-property-value-in-javascript
        names = self.productData();
        names.sort(function (a, b) { return (a.name > b.name) ? 1 : ((b.name > a.name) ? -1 : 0); });
        return names;
    });
    // Users
    self.userWatch = ko.observable(1);
    self.userData = ko.observableArray([]);
    self.userColumns = ko.observable(userColumnsOrder);
    self.userColumnMap = userColumnsMap;
    self.userColumns.subscribe(function () { self.userWatch(1 + self.userWatch()); });

    /* Client and Product Area multiselect functions and variables */
    self.defaultMultiselectOptions = {
        buttonWidth: '100%',
        buttonClass: 'btn btn-secondary',
        nableFiltering: true,
        enableCaseInsensitiveFiltering: true,
        includeSelectAllOption: true,
        selectAllNumber: false,
        templates: {
            filter: '<li class="multiselect-item filter"><div class="input-group pr-2"><span class="input-group-addon"><i class="fa fa-search"></i></span><input class="form-control multiselect-search" type="text"></div></li>',
            filterClearBtn: '<span class="input-group-btn"><button class="btn btn-secondary multiselect-clear-filter p-2" type="button"><i class="fa fa-times-circle"></i></button></span>'
        },
        onDropdownHidden: function (event) {
            var selectElement = $(event.target).prev();
            var selectID = selectElement.attr('id');
            var values = selectElement.val();
            for (var idx in values) {
                values[idx] = parseInt(values[idx]);
            }
            if (selectID.indexOf("Client") !== -1) {
                featureRequestViewModel.updateFilter("client", values);
            } else {
                featureRequestViewModel.updateFilter("product", values);
            }
        }
    }
    self.updateClientMultiselect = function (option, item) {
        if (item.id === self.clientNamesOrdered()[self.clientNamesOrdered().length - 1].id) {
            var element = $("#featureClientFilter");
            // Delay added due to problems it to work properly. :-(
            setTimeout(function () {
                element.multiselect('rebuild');
                element.multiselect('selectAll', false);
                element.multiselect('updateButtonText');
                // This is a manual trigger of the dropdown to update the filtered data.
                $("#featureClientFilterContainer").trigger("hidden.bs.dropdown");
            }, 500);
        }
    }
    self.updateProductMultiselect = function (option, item) {
        if (item.id === self.productNamesOrdered()[self.productNamesOrdered().length - 1].id) {
            var element = $("#featureProductFilter");
            // Delay added due to problems it to work properly. :-(
            setTimeout(function () {
                console.log("Delayed");
                element.multiselect('rebuild');
                element.multiselect('selectAll', false);
                element.multiselect('updateButtonText');
                // This is a manual trigger of the dropdown to update the filtered data.
                $("#featureProductFilterContainer").trigger("hidden.bs.dropdown");

            }, 500);
        }
    }

    // Had an issue with the slider not being callable, this is a workaround for now.
    self.sliderInit = false
    self.initSlider = function () {
        if (!self.sliderInit) {
            self.sliderInit = true;
            $("#slider-range").slider({
                range: true,
                min: self.featurePriorityMin(),
                max: self.featurePriorityMax(),
                values: [self.featurePriorityMin(), self.featurePriorityMax()],
                slide: function (event, ui) {
                    $("#sliderAmount").text("Priority Range: " + ui.values[0] + " - " + ui.values[1]);
                },
                stop: function (event, ui) {
                    console.log(ui.values);
                    featureRequestViewModel.updateFilter("priority", ui.values);
                }
            });
            $("#sliderAmount").text("Priority Range: " + $("#slider-range").slider("values", 0) + " - " + $("#slider-range").slider("values", 1));
        }
    }


    /* Sorting drag and drop - largely taken from the example. */
    self.dragAndDropSortableIterms = ["Client", "Priority", "Product Area", "Target Date"];
    function SortableView(items) {
        items = items || [];
        this.items = ko.observableArray([].concat(items));
        this.subscribedItems = ko.observableArray(this.items());
    }
    SortableView.prototype.self = self.sortable;
    SortableView.prototype.dragStart = function (item) {
        item.dragging(true);
    };
    SortableView.prototype.dragEnd = function (item) {
        item.self.sortable.subscribedItems(item.self.sortable.items());
        item.dragging(false);
    };
    SortableView.prototype.reorder = function (event, dragData, zoneData) {
        if (dragData !== zoneData.item) {
            var zoneDataIndex = zoneData.items.indexOf(zoneData.item);
            zoneData.items.remove(dragData);
            zoneData.items.splice(zoneDataIndex, 0, dragData);
        }
    };
    self.toDraggables = function(values) {
        return ko.utils.arrayMap(values, function (value) {
            return {
                self: self,
                value: value,
                dragging: ko.observable(false),
                isSelected: ko.observable(false),
                disbaled: false,
                startsWithVowel: function () {
                    return !!this.value.match(/^(a|e|i|o|u|y)/i);
                }
            };
        });
    }
    self.sortable = new SortableView(self.toDraggables(self.dragAndDropSortableIterms));
    self.sortable.subscribedItems.subscribe(function () {
        self.sortFeatureTable();
    });

    /*
     * Custom sorting function
     * Data can either be passed in (when filtering or getting fresh data)
     * or it can be pulled from the current dataset (sorting only).
     * Thanks to this guy for the awesome thenBy.js sorting library.
     * That made life substantially easier.
     * https://github.com/Teun/thenBy.js
     */
    self.sortFeatureTable = function (data) {
        if (typeof (data) === "undefined") {
            var data = self.featureData();
        }
        var mapper = {
            'Client': 'client',
            'Product Area': 'product_area',
            'Priority': 'priority',
            'Target Date': 'target_date'
        };
        var sortOrder = [];
        for (var idx in self.sortable.items()) {
            sortOrder.push(mapper[self.sortable.items()[idx].value]);
        }

        var sortingAlgorithm = firstBy(sortOrder[0]).thenBy(sortOrder[1]).thenBy(sortOrder[2]).thenBy(sortOrder[3]);
        data.sort(sortingAlgorithm);
        self.featureData(data);
    }
    /* Variables to hold filter data. */
    self.clientFilter = ko.observableArray([]);
    self.productFilter = ko.observableArray([]);
    self.priorityFilter = ko.observableArray([]);
    self.clientFilter.subscribe(function () {
        self.filterFeatureTable();
    });
    self.productFilter.subscribe(function () {
        self.filterFeatureTable();
    });
    self.priorityFilter.subscribe(function () {
        self.filterFeatureTable();
    });
    /* Function to prevent re-filtering data if nothing has changed. */
    self.updateFilter = function (filterType, data) {
        if (filterType === "client") {
            var oldData = self.clientFilter();
            if (oldData.length !== data.length) {
                self.clientFilter(data);
                return;
            }
            for (var idx in oldData) {
                if (oldData[idx] !== data[idx]) {
                    self.clientFilter(data);
                    return;
                }
            }
        } else if (filterType === "product") {
            var oldData = self.productFilter();
            if (oldData.length !== data.length) {
                self.productFilter(data);
                return;
            }
            for (var idx in oldData) {
                if (oldData[idx] !== data[idx]) {
                    self.productFilter(data);
                    return;
                }
            }
        } else if (filterType === "priority") {
            var oldData = self.priorityFilter();
            if (oldData.length !== data.length) {
                self.priorityFilter(data);
                return;
            }
            for (var idx in oldData) {
                if (oldData[idx] !== data[idx]) {
                    self.priorityFilter(data);
                    return;
                }
            }
        }
    }
    /*
     * Custom filtering function
     * Sets a disable flag when we don't want to see it.
     * This is perhaps the lazy solution. Enable everything
     * and then see what doesn't fit the filters.
     */
    self.filterFeatureTable = function (data, passToSort) {
        if (typeof (data) === "undefined") {
            var data = self.featureData();
        }
        for (var idx in data) {
            data[idx].enable = true;
            if ($.inArray(data[idx].client_id, self.clientFilter()) === -1) {
                data[idx].enable = false;
            }
            if ($.inArray(data[idx].product_id, self.productFilter()) === -1) {
                data[idx].enable = false;
            }
            if (data[idx].priority < self.priorityFilter()[0] || data[idx].priority > self.priorityFilter()[1]) {
                data[idx].enable = false;
            }
        }
        if (passToSort) {
            self.sortFeatureTable(data);
        } else {
            self.featureData(data);
        }
    }

    self.featureToggleDisplay = function (featureDataIdx) {
        var id = self.featureData()[featureDataIdx]["id"];
        var element = $("#showFeature_" + id);
        var visible = element.is(":visible");
        if (visible) {
            $(".featureExandableButton").removeClass("fa-caret-down");
            $(".featureExandableButton").addClass("fa-caret-right");
            $(".featureExpandable").hide();
        } else {
            // Check to see if we have data on this already.
            if (!("feature_" + id in self.featureDiscussionData())) {
                // We don't, so lets fetch it.
                $.get("featurenote/" + id, {}, function (data) {
                    if (data.hasOwnProperty('message')) {
                        // Convert to a better error display...
                        console.log("Sorry, you do not have permission to access this!");
                    } else {
                        data = data["feature_notes"];
                        // Change the date format
                        for (var i in data) {
                            data[i]['created'] = new moment(data[i]['created']).format("MMM D, YYYY [at] H:m A");
                        }
                        var allData = self.featureDiscussionData();
                        allData["feature_" + id] = data;
                        self.featureDiscussionData(allData);
                    }
                });
            }
            $("#featureExandableButton_" + id).removeClass("fa-caret-right");
            $("#featureExandableButton_" + id).addClass("fa-caret-down");
            $("#showFeature_" + id).show();
        }
    }
    self.featureDiscussionAddResponse = function (id) {
        console.log('AddResponse: ' + id);
        var json_data = $("#featureAddResponse_" + id).serializeJSON();
        var sendData = $.ajax({
            url: "featurenote",
            method: "POST",
            data: json_data,
            contentType: "application/json; charset=utf-8",
            dataType: "json"
        });
        sendData.done(function (msg) {
            $("#featureAddResponseText_" + id).val('');
            data = msg["feature_note"];
            data["created"] = new moment(data["created"]).format("MMM D, YYYY [at] H:m A");
            var allData = self.featureDiscussionData();
            allData["feature_" + id].push(data);
            self.featureDiscussionData(allData);
        });
    }

    /* Functions to get data from the API and pass it along*/
    self.getData = function(data_type) {
        $.get("/" + data_type, {}, function( data ) {
            if (data.hasOwnProperty('message')) {
                console.log("Sorry, you do not have permission to access this!");
                self[data_type + "Data"]([]);
            } else {
                if (data_type === "product") {
                    for (var i in data['products']) {
                        if (data['products'][i]['active'] == true) {
                            data['products'][i]['active'] = "Yes";
                        } else {
                            data['products'][i]['active'] = "No";
                        }
                    }
                }
                if (data_type === "feature") {
                    var minValue = Number.MAX_SAFE_INTEGER;
                    var maxValue = 0;
                    for (var idx in data["features"]) {
                        minValue = Math.min(data["features"][idx]["priority"], minValue);
                        maxValue = Math.max(data["features"][idx]["priority"], maxValue);
                        data["features"][idx]["created"] = new moment(data["features"][idx]["created"]).format("MMM D, YYYY [at] H:m A");
                    }
                    self.featurePriorityMin(minValue);
                    self.featurePriorityMax(maxValue);
                    self.filterFeatureTable(data["features"], true);
                } else {
                    self[data_type + "Data"](data[data_type + "s"]);
                }
            }
        });
    }
    self.updateData = function (data) {
        if (typeof (data) === "undefined") {
            self.getData('feature');
            self.getData('client');
            self.getData('product');
            self.getData('user');
        } else if (data == "feature") {
            self.getData('feature');
        } else if (data == "client") {
            self.getData('client');
        } else if (data == "product") {
            self.getData('product');
        } else if (data == "user") {
            self.getData('user');
        } else {
            console.log("Check spell check!");
        }
    }
};

var featureRequestViewModel = new FeatureRequestViewModel();
ko.applyBindings(featureRequestViewModel);

$(function () {
    /* Default options for the multiselects used for filtering. */
    var defaultMultiselectOptions = {
        buttonWidth: '100%',
        buttonClass: 'btn btn-secondary',
        nableFiltering: true,
        enableCaseInsensitiveFiltering: true,
        includeSelectAllOption: true,
        selectAllNumber: false,
        templates: {
            filter: '<li class="multiselect-item filter"><div class="input-group pr-2"><span class="input-group-addon"><i class="fa fa-search"></i></span><input class="form-control multiselect-search" type="text"></div></li>',
            filterClearBtn: '<span class="input-group-btn"><button class="btn btn-secondary multiselect-clear-filter p-2" type="button"><i class="fa fa-times-circle"></i></button></span>'
        },
        onDropdownHidden: function (event) {
            var selectElement = $(event.target).prev();
            var selectID = selectElement.attr('id');
            var values = selectElement.val();
            for (var idx in values) {
                values[idx] = parseInt(values[idx]);
            }
            if (selectID.indexOf("Client") !== -1) {
                featureRequestViewModel.updateFilter("client", values);
            } else {
                featureRequestViewModel.updateFilter("product", values);
            }
        }
    }
    $('#featureClientFilter').multiselect($.extend({}, defaultMultiselectOptions, {
        nonSelectedText: 'No Clients',
        allSelectedText: 'All Clients',
        buttonContainer: '<div class="btn-group m-2" id="featureClientFilterContainer" />',
    }));
    $('#featureProductFilter').multiselect($.extend({}, defaultMultiselectOptions, {
        nonSelectedText: 'No Products',
        allSelectedText: 'All Products',
        buttonContainer: '<div class="btn-group m-2" id="featureProductFilterContainer" />',
    }));

    $('[data-toggle="tooltip"]').tooltip({
        trigger: 'hover',
        template: '<div class="tooltip" role="tooltip"><div class="tooltip-arrow"></div><div class="tooltip-inner"></div></div>'
    });
    /*
    $("#slider-range").slider({
        range: true,
        min: 1,
        max: 10,
        values: [1, 10],
        slide: function (event, ui) {
            $("#sliderAmount").text("Priority Range: " + ui.values[0] + " - " + ui.values[1]);
        },
        stop: function (event, ui) {
            console.log(ui.values);
            featureRequestViewModel.updateFilter("priority", ui.values);
        }
    });*/
    //$("#sliderAmount").text("Priority Range: " + $("#slider-range").slider("values", 0) + " - " + $("#slider-range").slider("values", 1));
    
    featureRequestViewModel.updateData();
    featureRequestViewModel.initSlider();
});