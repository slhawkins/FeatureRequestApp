// Below are two types of structures for helping the client application
// The first structure is a map for converting from a field retrieved 
// from the RESTful API to a column title. Variables that end in 'Map'
// are of this type. The second structure is simply a default ordering
// of the columns. Using this allows me to setup a default column
// view which can be modified on a per-table basis.

var featureColumnsMap = {
    'client': 'Client',
    'client_id': 'Client ID',
    'created': 'Created',
    'description': 'Description',
    'id': 'ID',
    'priority': 'Priority',
    'product_area': 'Product Area',
    'product_id': 'Product ID',
    'target_date': 'Target Date',
    'ticket_url': 'Ticket URL',
    'title': 'Title',
    'user': 'User' ,
    'user_id': 'User ID'
};

var featureColumnsOrder = [
    'client',
    'product_area',
    'title',
    'priority',
    'target_date'
];

var clientColumnsMap = {
    'created': 'Created',
    'email': 'Email',
    'id': 'ID',
    'name': 'Name',
    'phone': 'Phone',
    'poc': 'Poc',
    'user': 'User',
    'user_id': 'User ID'
};

var clientColumnsOrder = [
    'name',
    'poc',
    'email',
    'phone'
];

var productColumnsMap = {
    'created': 'Created',
    'description': 'Description',
    'id': 'ID',
    'name': 'Name',
    'user': 'User',
    'user_id': 'User ID',
    'active': 'Active'
};

var productColumnsOrder = [
    'name',
    'description',
    'active'
];

var userColumnsMap = {
    'id': 'ID',
    'role': 'Role',
    'username': 'Username'
};

var userColumnsOrder = [
    'id',
    'username',
    'role'
];