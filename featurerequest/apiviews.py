"""Provides all RESTful API calls via Flask-RESTful"""
from datetime import datetime
from featurerequest import app, db
from featurerequest.user_auth import roles, roles_advanced
from featurerequest.models import \
    User, UserSchema,\
    Client, ClientSchema,\
    Product, ProductSchema,\
    Feature, FeatureSchema,\
    FeatureComment, FeatureCommentSchema
from flask import jsonify, request, make_response
from flask_restful import Api, Resource
from flask_login import current_user
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func
from marshmallow.exceptions import ValidationError

api = Api(app) # pylint: disable=invalid-name

# Used to prevent the RESTful methods from being flagged.
# pylint: disable=no-self-use
class BaseAPI(Resource):
    """Provides a custom base for all resources to use, helping to minimize code use."""

    def __init__(self, *args, **kwargs):
        super(Resource, self).__init__(*args, **kwargs)
        self.resource_url = ''
        self.role_list = {
            'get': [],
            'post': [],
            'put': [],
            'delete': []
        }
        self.resource_name = ''
        self.single_item = ''
        self.multiple_items = ''
        self.table = None
        self.schema = None
        self.schema_many = None
        self.put_check_message = ''



    @roles_advanced('get')
    def get(self, id=None):
        """Returns a list of all resources ir the resource belonging to the id."""
        if id is None:
            query = self.table.query.all()
            results = self.schema_many.dump(query)
            return make_response(jsonify({self.multiple_items: results.data}), 200)
        query = self.table.query.get_or_404(id)
        result = self.schema.dump(query)
        return make_response(jsonify({self.single_item: result.data}), 200)

    @roles_advanced('post')
    def post(self):
        """Adds a resource and returns the added database entry."""
        json_data = request.get_json()
        if not json_data:
            return make_response(jsonify({'message': 'No data provided'}), 400)
        data, errors = self.schema.load(json_data)
        if errors:
            return make_response(jsonify(errors), 400)
        data.user_id = current_user.id
        db.session.add(data)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return make_response(jsonify({'message': self.resource_name +
                                          ' is already in the database!'}), 400)
        result = self.schema.dump(self.table.query.get_or_404(data.id))
        return make_response(jsonify({'message': 'Added the ' + self.resource_name + '.',
                                     self.single_item: result.data}), 201)

    @roles_advanced('put')
    def put(self, id=None):
        """Updates a resource and returns the updated entry."""
        if not id:
            return make_response(jsonify({
                'message': 'You must supply an id in the URI.'}), 400)
        try:
            safe = self.put_check(id)
            if not safe:
                return make_response(jsonify({
                'message': self.put_check_message}), 400)
        except AttributeError: # Happens if self.put_check() isn't defined. EAFP!
            pass
        json_data = request.get_json()
        if not json_data:
            return make_response(jsonify({'message': 'No data provided'}), 400)
        data = self.table.query.get_or_404(id)
        try:
            for key, value in json_data.items():
                self.schema.validate({key:value})
                setattr(data, key, value)
                db.session.commit()
        except ValidationError as err:
            db.session.rollback()
            return make_response(jsonify({'message': err.messages}), 400)
        result = self.schema.dump(self.table.query.get_or_404(data.id))
        return make_response(jsonify({'message': 'Updated the ' + self.resource_name + '.',
                                      self.single_item: result.data}), 200)


class UserAPI(BaseAPI):
    """Provides the 'user' resource.

    get/<user_id>:
        Return a list of users or the user belonging to the user_id.

    post:
        Adds a new user, returns the added database entry.

    put/<user_id>:
        Updates the user.

    delete/<user_id>:
        Sets the specified user to 'Inactive', preventing them from using the service.
    """
    def __init__(self, *args, **kwargs):
        super(BaseAPI, self).__init__(*args, **kwargs)
        self.resource_url = ''
        self.role_list = {
            'get': ['Employee', 'Administrator'],
            'post': ['Administrator'],
            'put': ['Administrator'],
            'delete': ['Administrator']
        }
        self.resource_name = 'User'
        self.single_item = 'user'
        self.multiple_items = 'users'
        self.table = User
        self.schema = UserSchema()
        self.schema_many = UserSchema(many=True)
        self.put_check_message = 'You cannot modify your own attributes.'

    def put_check(self, id):
        if current_user.id == id:
            return False
        return True

    @roles('Administrator')
    def delete(self, id=None):
        if not id:
            return make_response(jsonify({
                'message': 'You cannot modify your own attributes.'}), 400)
        """Sets the specified user to 'Inactive', preventing them from using the service."""
        if current_user.id == id:
            return make_response(jsonify({
                'message': 'You cannot modify your own attributes.'}), 400)
        data = User.query.get_or_404(id)
        data.role = 'Inactive'
        db.session.commit()
        return make_response(jsonify({'message': 'Set the user to inactive.',
                                      'user': {'username': data.username}}), 200)

class ClientAPI(BaseAPI):
    """Provides the 'client' resource.

    get/<client_id>:
        Return a list of clients or the client belonging to the client_id.

    post:
        Adds a new client, returns the added database entry.

    put/<client_id>:
        Updates the client.

    delete/<client_id>:
        Remove the client and all data associated with it.
    """
    def __init__(self, *args, **kwargs):
        super(BaseAPI, self).__init__(*args, **kwargs)
        self.resource_url = ''
        self.role_list = {
            'get': ['Employee', 'Administrator'],
            'post': ['Administrator'],
            'put': ['Administrator'],
            'delete': ['Administrator']
        }
        self.resource_name = 'Client'
        self.single_item = 'client'
        self.multiple_items = 'clients'
        self.table = Client
        self.schema = ClientSchema()
        self.schema_many = ClientSchema(many=True)

    @roles('Administrator')
    def delete(self, id=None):
        """Remove the client and all data associated with it."""
        if not id:
            return make_response(jsonify({
                'message': 'You must supply an id in the URI.'}), 400)
        data = Client.query.get_or_404(id)
        name = data.name
        # Remove all dependencies
        feature_ids = [x[0] for x in db.session.query(Feature.id).\
            filter_by(client_id=id).all()]
        for feature_id in feature_ids:
            db.session.query(FeatureComment).filter_by(feature_id=feature_id).delete()
        db.session.query(Feature).filter_by(client_id=id).delete()
        db.session.query(Client).filter_by(id=id).delete()
        db.session.commit()
        return make_response(jsonify({'message': 'Removed a client.',
                                      'client': {'name': name}}), 200)


class ProductAPI(Resource):
    """Provides the 'product' resource.

    get/<product_id>:
        Return a list of products or the product belonging to the product_id.

    post:
        Adds a new client, returns the added database entry.

    put/<product_id>:
        Updates the product.

    delete/<product_id>:
        Sets the product to inactive. Prevents it from being used by new features
        but does not impact existing features.
    """
    @roles('Employee', 'Administrator')
    def get(self, product_id=None):
        """Return a list of products or the product belonging to the product_id."""
        if product_id is None:
            products = Product.query.all()
            results = ProductSchema(many=True).dump(products)
            return make_response(jsonify({'products': results.data}), 200)
        product = Product.query.get(product_id)
        result = ProductSchema().dump(product)
        return make_response(jsonify({'product': result.data}), 200)

    @roles('Administrator')
    def post(self):
        """Adds a new client, returns the added database entry."""
        schema = ProductSchema()
        json_data = request.get_json()
        if not json_data:
            return make_response(jsonify({'message': 'No data provided'}), 400)
        data, errors = schema.load(json_data)
        if errors:
            return make_response(jsonify(errors), 422)
        data.user_id = current_user.id
        db.session.add(data)
        db.session.commit()
        result = schema.dump(Product.query.get(data.id))
        return make_response(jsonify({'message': 'Added a product.',
                                      'product': result.data}), 201)

    @roles('Administrator')
    def put(self, product_id):
        """Updates the product."""
        schema = ProductSchema()
        json_data = request.get_json()
        if not json_data:
            return make_response(jsonify({'message': 'No data provided'}), 400)
        data = Product.query.get_or_404(product_id)
        try:
            for key, value in json_data.items():
                schema.validate({key:value})
                setattr(data, key, value)
                db.session.commit()
        except ValidationError as err:
            return make_response(jsonify({'message': err.messages}), 400)
        result = schema.dump(Product.query.get(data.id))
        return make_response(jsonify({'message': 'Updated a product.',
                                      'product': result.data}), 200)

    @roles('Administrator')
    def delete(self, product_id):
        """Sets the product to inactive. Prevents it from being used by new features
        but does not impact existing features.
        """
        data = Product.query.get_or_404(product_id)
        data.active = False
        db.session.commit()
        return make_response(jsonify({'message': 'Deactivated the product area.',
                                      'product': {'name': data.name}}), 200)

class FeatureAPI(Resource):
    """Provides the 'feature' resource.

    get/<feature_id>:
        Return a list of features or the feature belonging to the feature_id.

    post:
        Adds a new feature, returns the added database entry.

    put/<feature_id>:
        Updates the feature.

    delete/<feature_id>:
        Remove the feature and all data associated with it.
    """
    @roles('Employee', 'Administrator')
    def get(self, feature_id=None):
        """Return a list of features or the feature belonging to the feature_id."""
        if feature_id is None:
            features = Feature.query.all()
            results = FeatureSchema(many=True).dump(features)
            return make_response(jsonify({'features': results.data}), 200)
        feature = Feature.query.get(feature_id)
        result = FeatureSchema().dump(feature)
        return make_response(jsonify({'feature': result.data}), 200)

    @roles('Employee', 'Administrator')
    def post(self):
        """Adds a new feature, returns the added database entry."""
        schema = FeatureSchema()
        json_data = request.get_json()
        if not json_data:
            return make_response(jsonify({'message': 'No data provided'}), 400)
        if 'target_date' in json_data:
            if json_data['target_date'] != "":
                json_data['target_date'] = str(datetime.strptime(json_data['target_date'],
                                                                 "%m/%d/%Y").strftime("%Y-%m-%d"))
            else:
                del json_data['target_date']
        data, errors = schema.load(json_data)
        if errors:
            return make_response(jsonify(errors), 422)
        # Update the priority when needed.
        results = Feature.query.filter(Feature.client_id == json_data['client_id']).\
            filter(Feature.priority >= json_data['priority']).all()
        if results:
            for row in results:
                row.priority += 1
            db.session.commit()
        else:
            results = db.session.query(func.max(Feature.priority)).\
                filter(Feature.client_id == json_data['client_id']).all()
            max_priority = results[0][0]
            if max_priority is None:
                data.priority = 1
            else:
                data.priority = max_priority + 1
        data.user_id = current_user.id
        db.session.add(data)
        db.session.commit()
        result = schema.dump(Feature.query.get(data.id))
        return make_response(jsonify({'message': 'Added a feature.', 'feature': result.data}), 201)

    @roles('Employee', 'Administrator')
    def put(self, feature_id):
        """Updates the feature."""
        schema = FeatureSchema()
        json_data = request.get_json()
        if json_data['target_date'] != "":
            json_data['target_date'] = str(datetime.strptime(json_data['target_date'],
                                                             "%m/%d/%Y").strftime("%Y-%m-%d"))
        else:
            del json_data['target_date']
        if not json_data:
            return make_response(jsonify({'message': 'No data provided'}), 400)
        data = Feature.query.get_or_404(feature_id)
        priority = int(json_data['priority'])
        if priority != data.priority:
            # Changing the priority... Lets move everything down if needed.
            results = Feature.query.filter(Feature.client_id == json_data['client_id']).\
                filter(Feature.priority > data.priority).all()
            for row in results:
                row.priority -= 1
            db.session.commit()
            # Now move everything forward for the new priority...
            results = Feature.query.filter(Feature.client_id == json_data['client_id']).\
                filter(Feature.priority >= priority).all()
            if results:
                for row in results:
                    row.priority += 1
                db.session.commit()
            results = db.session.query(func.max(Feature.priority)).\
                filter(Feature.client_id == int(json_data['client_id'])).all()
            max_priority = results[0][0]
            if max_priority is None:
                json_data['priority'] = 1
            else:
                if priority > max_priority:
                    json_data['priority'] = max_priority + 1
        del json_data['client_id']
        try:
            for key, value in json_data.items():
                schema.validate({key:value})
                setattr(data, key, value)
                db.session.commit()
        except ValidationError as err:
            return make_response(jsonify({'message': err.messages}), 400)
        result = schema.dump(Feature.query.get(data.id))
        return make_response(jsonify({'message': 'Updated a feature.',
                                      'feature': result.data}), 200)

    @roles('Employee', 'Administrator')
    def delete(self, feature_id):
        """Remove the feature and all data associated with it."""
        data = Feature.query.get_or_404(feature_id)
        title = data.title
        priority = data.priority
        client_id = data.client_id
        results = Feature.query.filter(Feature.client_id == client_id).\
            filter(Feature.priority > priority).all()
        for row in results:
            row.priority -= 1
        db.session.commit()
        db.session.query(FeatureComment).filter_by(feature_id=feature_id).delete()
        db.session.query(Feature).filter_by(id=feature_id).delete()
        db.session.commit()
        return make_response(jsonify({'message': 'Removed a feature.',
                                      'feature': {'title': title}}), 200)


class FeatureCommentAPI(Resource):
    """Provides the 'feature_comment' resource.

    get/<feature_id>:
        Return a list of all feature_comments or a list of those belonging to feature_id.

    post:
        Adds a new feature comment, returns the added data.
    """
    @roles('Employee', 'Administrator')
    def get(self, feature_id=None):
        """Return a list of all feature_comments or a list of those belonging to feature_id."""
        if feature_id is None:
            feature_notes = FeatureComment.query.all()
            results = FeatureCommentSchema(many=True).dump(feature_notes)
            return make_response(jsonify({'feature_notes': results.data}), 200)
        feature_note = FeatureComment.query.\
            filter(FeatureComment.feature_id == feature_id).all()
        result = FeatureCommentSchema(many=True).dump(feature_note)
        return make_response(jsonify({'feature_notes': result.data}), 200)

    @roles('Employee', 'Administrator')
    def post(self):
        """Adds a new feature comment, returns the added data."""
        schema = FeatureCommentSchema()
        json_data = request.get_json()
        if not json_data:
            return make_response(jsonify({'message': 'No data provided'}), 400)
        data, errors = schema.load(json_data)
        if errors:
            return make_response(jsonify(errors), 422)
        data.user_id = current_user.id
        db.session.add(data)
        db.session.commit()
        result = schema.dump(FeatureComment.query.get(data.id))
        return make_response(jsonify({'message': 'Added a feature note.',
                                      'feature_note': result.data}), 201)


api.add_resource(UserAPI, '/user', '/user/<int:id>', endpoint='user')
api.add_resource(ClientAPI, '/client', '/client/<int:id>', endpoint='client')
api.add_resource(ProductAPI, '/product', '/product/<int:product_id>', endpoint='product')
api.add_resource(FeatureAPI, '/feature', '/feature/<int:feature_id>', endpoint='feature')
api.add_resource(FeatureCommentAPI, '/feature_comment', '/feature_comment/<int:feature_id>',
                 endpoint='feature_comment')
