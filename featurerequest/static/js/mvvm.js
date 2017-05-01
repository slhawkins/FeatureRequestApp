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
    // Following these, I place subscribe to the data and column observables.
    // 
    // Features
    self.featureWatch = ko.observable(1);
    self.featureData = ko.observable({ 'features': [] });
    self.featureColumns = ko.observable(featureColumnsOrder);
    self.featureColumnMap = featureColumnsMap;
    self.featureData.subscribe(function () { self.featureWatch(1 + self.featureWatch()); });
    self.featureColumns.subscribe(function () { self.featureWatch(1 + self.featureWatch()); });
    // Clients
    self.clientWatch = ko.observable(1);
    self.clientData = ko.observable({ 'clients': [] });
    self.clientColumns = ko.observable(clientColumnsOrder);
    self.clientColumnMap = clientColumnsMap;
    self.clientData.subscribe(function () { self.clientWatch(1 + self.clientWatch()); });
    self.clientColumns.subscribe(function () { self.clientWatch(1 + self.clientWatch()); });
    // Products
    self.productWatch = ko.observable(1);
    self.productData = ko.observable({ 'products': [] });
    self.productColumns = ko.observable(productColumnsOrder);
    self.productColumnMap = productColumnsMap;
    self.productData.subscribe(function () { self.productWatch(1 + self.productWatch()); });
    self.productColumns.subscribe(function () { self.productWatch(1 + self.productWatch()); });
    // Users
    self.userWatch = ko.observable(1);
    self.userData = ko.observable({ 'users': [] });
    self.userColumns = ko.observable(userColumnsOrder);
    self.userColumnMap = userColumnsMap;
    self.userData.subscribe(function () { self.userWatch(1 + self.userWatch()); });
    self.userColumns.subscribe(function () { self.userWatch(1 + self.userWatch()); });

    self.updateData = function (data) {
        if (typeof (data) === "undefined") {
            $.get("/feature", {}, self.featureData);
            $.get("/client", {}, self.clientData);
            $.get("/product", {}, self.productData);
            $.get("/user", {}, self.userData);
        } else if (data == "feature") {
            $.get("/feature", {}, self.featureData);
        } else if (data == "client") {
            $.get("/client", {}, self.clientData);
        } else if (data == "product") {
            $.get("/product", {}, self.productData);
        } else if (data == "user") {
            $.get("/user", {}, self.userData);
        } else {
            console.log("Check spell check!");
        }
    }
    self.updateData();
};

var featureRequestViewModel = new FeatureRequestViewModel();
ko.applyBindings(featureRequestViewModel);