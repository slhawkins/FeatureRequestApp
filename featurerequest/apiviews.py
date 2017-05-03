"""Provides all RESTful API calls via Flask-RESTful"""
from datetime import datetime
from featurerequest import app, db
from featurerequest.user_auth import roles
from featurerequest.models import \
    User, UserSchema,\
    Client, ClientSchema,\
    ClientNote, ClientNoteSchema,\
    Product, ProductSchema,\
    Feature, FeatureSchema,\
    FeatureTodo, FeatureTodoSchema,\
    FeatureNote, FeatureNoteSchema
from flask import jsonify, request, make_response
from flask_restful import Api, Resource
from flask_login import current_user, login_user
from sqlalchemy.orm import contains_eager
from sqlalchemy.exc import IntegrityError
from marshmallow.exceptions import ValidationError

api = Api(app)

class UserAPI(Resource):
    @roles('Employee', 'Administrator')
    def get(self, id=None):
        if id is None:
            users = User.query.all()
            results = UserSchema(many=True).dump(users)
            return make_response(jsonify({'users': results.data}), 200)
        else:
            user = User.query.get(id)
            result = UserSchema().dump(user)
            return make_response(jsonify({'user': result.data}), 200)

    @roles('Administrator')
    def post(self):
        schema = UserSchema()
        json_data = request.get_json()
        if not json_data:
            return make_response(jsonify({'message': 'No data provided'}), 400)
        data, errors = schema.load(json_data)
        if errors:
            return make_response(jsonify(errors), 422)
        data.user_id = current_user.id
        db.session.add(data)
        try:
            db.session.commit()
        except IntegrityError:
            return make_response(jsonify({'message': 'Username already in the database!'}), 400)
        print(data.username)
        result = schema.dump(User.query.get(data.id))
        print(result)
        return make_response(jsonify({'message': 'Added a user.', 'user': result.data}), 201)

    @roles('Administrator')
    def put(self, id):
        if current_user.id == id:
            return make_response(jsonify({'message': 'You cannot modify your own attributes.'}), 400)
        schema = UserSchema()
        json_data = request.get_json()
        if not json_data:
            return make_response(jsonify({'message': 'No data provided'}), 400)
        data = User.query.get_or_404(json_data['id'])
        try:
            for key, value in json_data.items():
                schema.validate({key:value})
                setattr(data, key, value)
                db.session.commit()
        except ValidationError as err:
            return make_response(jsonify({'message': err.message}), 400)
        result = schema.dump(User.query.get(data.id))
        print(result)
        return make_response(jsonify({'message': 'Updated a user.', 'user': result.data}), 201)


class ClientAPI(Resource):
    @roles('Employee', 'Administrator')
    def get(self, id=None):
        if id is None:
            clients = Client.query.all()
            results = ClientSchema(many=True).dump(clients)
            return make_response(jsonify({'clients': results.data}), 200)
        else:
            client = Client.query.get(id)
            result = ClientSchema().dump(client)
            return make_response(jsonify({'client': result.data}), 200)

    @roles('Administrator')
    def post(self):
        schema = ClientSchema()
        json_data = request.get_json()
        if not json_data:
            return make_response(jsonify({'message': 'No data provided'}), 400)
        data, errors = schema.load(json_data)
        if errors:
            return make_response(jsonify(errors), 422)
        data.user_id = current_user.id
        db.session.add(data)
        db.session.commit()
        result = schema.dump(Client.query.get(data.id))
        return make_response(jsonify({'message': 'Added a client.', 'client': result.data}), 201)

    @roles('Administrator')
    def put(self, id):
        schema = ClientSchema()
        json_data = request.get_json()
        if not json_data:
            return make_response(jsonify({'message': 'No data provided'}), 400)
        data = Client.query.get_or_404(json_data['id'])
        try:
            for key, value in json_data.items():
                schema.validate({key:value})
                setattr(data, key, value)
                db.session.commit()
        except ValidationError as err:
            return make_response(jsonify({'message': err.message}), 400)
        result = schema.dump(Client.query.get(data.id))
        print(result)
        return make_response(jsonify({'message': 'Updated a client.', 'client': result.data}), 201)


class ClientNoteAPI(Resource):
    @roles('Employee', 'Administrator')
    def get(self, id=None):
        if id is None:
            client_notes = ClientNote.query.all()
            results = ClientNoteSchema(many=True).dump(client_notes)
            return make_response(jsonify({'client_notes': results.data}), 200)
        else:
            client_note = ClientNote.query.get(id)
            result = ClientNoteSchema().dump(client_note)
            return make_response(jsonify({'client_note': result.data}), 200)

    @roles('Employee', 'Administrator')
    def post(self):
        schema = ClientNoteSchema()
        json_data = request.get_json()
        if not json_data:
            return make_response(jsonify({'message': 'No data provided'}), 400)
        data, errors = schema.load(json_data)
        if errors:
            return make_response(jsonify(errors), 422)
        data.user_id = current_user.id
        db.session.add(data)
        db.session.commit()
        result = schema.dump(ClientNote.query.get(data.id))
        return make_response(jsonify({'message': 'Added a client note.', 'clientnote': result.data}), 201)


class ProductAPI(Resource):
    @roles('Employee', 'Administrator')
    def get(self, id=None):
        if id is None:
            products = Product.query.all()
            results = ProductSchema(many=True).dump(products)
            return make_response(jsonify({'products': results.data}), 200)
        else:
            product = Product.query.get(id)
            result = ProductSchema().dump(product)
            return make_response(jsonify({'product': result.data}), 200)

    @roles('Administrator')
    def post(self):
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
        return make_response(jsonify({'message': 'Added a product.', 'product': result.data}), 201)

    @roles('Administrator')
    def put(self, id):
        schema = ProductSchema()
        json_data = request.get_json()
        if not json_data:
            return make_response(jsonify({'message': 'No data provided'}), 400)
        data = Product.query.get_or_404(json_data['id'])
        try:
            for key, value in json_data.items():
                schema.validate({key:value})
                setattr(data, key, value)
                db.session.commit()
        except ValidationError as err:
            return make_response(jsonify({'message': err.message}), 400)
        result = schema.dump(Product.query.get(data.id))
        print(result)
        return make_response(jsonify({'message': 'Updated a product.', 'product': result.data}), 201)

class FeatureAPI(Resource):
    @roles('Employee', 'Administrator')
    def get(self, id=None):
        """
        Gets one or more features requests along with associated data.
        """
        if id is None:
            features = Feature.query.all()
            results = FeatureSchema(many=True).dump(features)
            return make_response(jsonify({'features': results.data}), 200)
        else:
            feature = Feature.query.get(id)
            result = FeatureSchema().dump(feature)
            return make_response(jsonify({'feature': result.data}), 200)

    @roles('Employee', 'Administrator')
    def post(self):
        schema = FeatureSchema()
        json_data = request.get_json()
        if not json_data:
            return make_response(jsonify({'message': 'No data provided'}), 400)
        # Update the priority when needed.
        results = Feature.query.filter(Feature.client_id == json_data['client_id']).filter(Feature.priority >= json_data['priority']).all()
        for row in results:
            row.priority += 1
        db.session.commit()
        data, errors = schema.load(json_data)
        if errors:
            return make_response(jsonify(errors), 422)
        data.user_id = current_user.id
        db.session.add(data)
        db.session.commit()
        result = schema.dump(Feature.query.get(data.id))
        return make_response(jsonify({'message': 'Added a feature.', 'feature': result.data}), 201)

    @roles('Employee', 'Administrator')
    def put(self, id):
        schema = FeatureSchema()
        json_data = request.get_json()
        if json_data['target_date'] != "":
            json_data['target_date'] = str(datetime.strptime(json_data['target_date'], "%m/%d/%Y").strftime("%Y-%m-%d"))
        if not json_data:
            return make_response(jsonify({'message': 'No data provided'}), 400)
        data = Feature.query.get_or_404(json_data['id'])
        try:
            for key, value in json_data.items():
                schema.validate({key:value})
                setattr(data, key, value)
                db.session.commit()
        except ValidationError as err:
            return make_response(jsonify({'message': err.message}), 400)
        result = schema.dump(Feature.query.get(data.id))
        print(result)
        return make_response(jsonify({'message': 'Updated a feature.', 'feature': result.data}), 201)


class FeatureTodoAPI(Resource):
    @roles('Employee', 'Administrator')
    def get(self, id=None):
        if id is None:
            feature_todos = FeatureTodo.query.all()
            results = FeatureTodoSchema(many=True).dump(feature_todos)
            return make_response(jsonify({'feature_todos': results.data}), 200)
        else:
            feature_todo = FeatureTodo.query.get(id)
            result = FeatureTodoSchema().dump(feature_todo)
            return make_response(jsonify({'feature_todo': result.data}), 200)

    @roles('Employee', 'Administrator')
    def post(self):
        schema = FeatureTodoSchema()
        json_data = request.get_json()
        if not json_data:
            return make_response(jsonify({'message': 'No data provided'}), 400)
        data, errors = schema.load(json_data)
        if errors:
            return make_response(jsonify(errors), 422)
        data.user_id = current_user.id
        db.session.add(data)
        db.session.commit()
        result = schema.dump(FeatureTodo.query.get(data.id))
        return make_response(jsonify({'message': 'Added a feature to-do.', 'feature_todo': result.data}), 201)


class FeatureNoteAPI(Resource):
    @roles('Employee', 'Administrator')
    def get(self, id=None):
        if id is None:
            feature_notes = FeatureNote.query.all()
            results = FeatureNoteSchema(many=True).dump(feature_notes)
            return make_response(jsonify({'feature_notes': results.data}), 200)
        else:
            feature_note = FeatureNote.query.get(id)
            result = FeatureNoteSchema().dump(feature_note)
            return make_response(jsonify({'feature_note': result.data}), 200)

    @roles('Employee', 'Administrator')
    def post(self):
        schema = FeatureNoteSchema()
        json_data = request.get_json()
        if not json_data:
            return make_response(jsonify({'message': 'No data provided'}), 400)
        data, errors = schema.load(json_data)
        if errors:
            return make_response(jsonify(errors), 422)
        data.user_id = current_user.id
        db.session.add(data)
        db.session.commit()
        result = schema.dump(FeatureNote.query.get(data.id))
        return make_response(jsonify({'message': 'Added a feature note.', 'feature_note': result.data}), 201)


api.add_resource(UserAPI, '/user', '/user/<int:id>', endpoint='user')
api.add_resource(ClientAPI, '/client', '/client/<int:id>', endpoint='client')
api.add_resource(ClientNoteAPI, '/clientnote', '/clientnote/<int:id>', endpoint='clientnote')
api.add_resource(ProductAPI, '/product', '/product/<int:id>', endpoint='product')
api.add_resource(FeatureAPI, '/feature', '/feature/<int:id>', endpoint='feature')
api.add_resource(FeatureTodoAPI, '/featuretodo', '/featuretodo/<int:id>', endpoint='featuretodo')
api.add_resource(FeatureNoteAPI, '/featurenote', '/featurenote/<int:id>', endpoint='featurenote')