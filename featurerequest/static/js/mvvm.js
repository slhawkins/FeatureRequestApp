function FeatureRequestViewModel() {
    var self = this;
    // Setup data observables. They have the following types:
    // _____Watch    : Watch variables are used to update the data table when
    //                 either its column order or data has changed. Listeners 
    //                 are placed on both of those observables.
    //                 I'm not 100% it was needed, but it was a fun exercise.
    // _____Data     : Data retrieved from the API
    // _____Columns  : Column order, will be modifiable 
    // _____ColumnMap: Contains a map from the field names retrieved via the API
    //                 to column titles.
    // Following these, I subscribe to the data and column observables.
    // 
    // Features
    self.featureWatch = ko.observable(1);
    self.featureData = ko.observableArray([]);
    self.featureColumns = ko.observable(featureColumnsOrder);
    self.featureColumnMap = featureColumnsMap;
    //self.featureData.subscribe(function () { self.featureWatch(1 + self.featureWatch()); });
    self.featureColumns.subscribe(function () { self.featureWatch(1 + self.featureWatch()); });
    // Clients
    self.clientWatch = ko.observable(1);
    self.clientData = ko.observableArray([]);
    self.clientColumns = ko.observable(clientColumnsOrder);
    self.clientColumnMap = clientColumnsMap;
    self.clientData.subscribe(function () { self.clientWatch(1 + self.clientWatch()); });
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
    self.productData.subscribe(function () { self.productWatch(1 + self.productWatch()); });
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
    self.userData.subscribe(function () { self.userWatch(1 + self.userWatch()); });
    self.userColumns.subscribe(function () { self.userWatch(1 + self.userWatch()); });

    self.getData = function(data_type) {
        $.get("/" + data_type, {}, function( data ) {
            if (data.hasOwnProperty('message')) {
                console.log("Sorry, you do not have permission to access this!");
                self[data_type + "Data"]([]);
            } else {
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