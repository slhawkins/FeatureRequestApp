function FeatureRequestViewModel() {
    var self = this;
    self.initialSetup = true;
    // Setup data observables. They have the following types:
    // _____Watch    : Watch variables are used to update the data table when
    //                 either its column order or data has changed. 
    // _____Data     : Data retrieved from the API
    // _____Columns  : Column order, will be modifiable 
    // _____ColumnMap: Contains a map from the field names retrieved via the API
    //                 to column titles.
    // 
    // Features
    self.featureWatch = ko.observable(1);
    self.featureData = ko.observableArray([]);
    self.featureColumns = ko.observable(featureColumnsOrder);
    self.featureColumnMap = featureColumnsMap;
    self.featureColumns.subscribe(function () { self.featureWatch(1 + self.featureWatch()); });
    self.featurePriorityMin = ko.pureComputed(function () {
        return 1;
    });
    self.featurePriorityMax = ko.pureComputed(function () {
        return 10;
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

    // Client and Product Area multiselect functions
    // These first check whether we're on the last element of the array
    // and then rebuilds the multiselect if we are.
    self.updateClientMultiselect = function (option, item) {
        if (item.id === self.clientNamesOrdered()[self.clientNamesOrdered().length - 1].id) {
            var element = $("#featureClientFilter");
            element.multiselect('rebuild');
            if (self.initialSetup) { // We only need to select all on startup.
                element.multiselect('selectAll', false);
                element.multiselect('updateButtonText');
            }
        }
    }
    self.updateProductMultiselect = function (option, item) {
        if (item.id === self.productNamesOrdered()[self.productNamesOrdered().length - 1].id) {
            var element = $("#featureProductFilter");
            element.multiselect('rebuild');
            if (self.initialSetup) { // We only need to select all on startup.
                element.multiselect('selectAll', false);
                element.multiselect('updateButtonText');
            }
        }
    }

    // Sorting drag and drop
    self.dragAndDropSortableIterms = ["Client", "Priority", "Product"];
    function SortableView(items) {
        items = items || [];
        this.items = ko.observableArray([].concat(items));
    }

    SortableView.prototype.dragStart = function (item) {
        item.dragging(true);
    };

    SortableView.prototype.dragEnd = function (item) {
        item.dragging(false);
    };

    SortableView.prototype.reorder = function (event, dragData, zoneData) {
        if (dragData !== zoneData.item) {
            var zoneDataIndex = zoneData.items.indexOf(zoneData.item);
            zoneData.items.remove(dragData);
            zoneData.items.splice(zoneDataIndex, 0, dragData);
        }
    };
    function toDraggables(values) {
        return ko.utils.arrayMap(values, function (value) {
            return {
                value: value,
                dragging: ko.observable(false),
                isSelected: ko.observable(false),
                startsWithVowel: function () {
                    return !!this.value.match(/^(a|e|i|o|u|y)/i);
                }
            };
        });
    }

    self.sortable = new SortableView(toDraggables(self.dragAndDropSortableIterms)),

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
                self[data_type + "Data"](data[data_type + "s"]);
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
    self.updateData();
};

var featureRequestViewModel = new FeatureRequestViewModel();
ko.applyBindings(featureRequestViewModel);

$(document).ready(function () {
    var defaultMultiselectOptions = {
        buttonWidth: '100%',
        buttonContainer: '<div class="btn-group m-2" />',
        buttonClass: 'btn btn-secondary',
        nableFiltering: true,
        enableCaseInsensitiveFiltering: true,
        includeSelectAllOption: true,
        selectAllNumber: false,
        templates: {
            filter: '<li class="multiselect-item filter"><div class="input-group pr-2"><span class="input-group-addon"><i class="fa fa-search"></i></span><input class="form-control multiselect-search" type="text"></div></li>',
            filterClearBtn: '<span class="input-group-btn"><button class="btn btn-secondary multiselect-clear-filter p-2" type="button"><i class="fa fa-times-circle"></i></button></span>'
        }
    }
    $('#featureClientFilter').multiselect($.extend({}, defaultMultiselectOptions, {
        nonSelectedText: 'No Clients',
        allSelectedText: 'All Clients'
    }));
    $('#featureProductFilter').multiselect($.extend({}, defaultMultiselectOptions, {
        nonSelectedText: 'No Products',
        allSelectedText: 'All Products'
    }));

    setTimeout(function () {
        $("#featurePrioritySlider").slider("relayout");
    }, 500);
});