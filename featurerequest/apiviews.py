"""Provides all RESTful API calls via Flask-RESTful"""
from featurerequest import app, db
from featurerequest.user_auth import roles
from featurerequest.models import \
    User, UserSchema,\
    Client, ClientSchema,\
    ClientNote, ClientNoteSchema,\
    ProductArea, ProductAreaSchema,\
    Feature, FeatureSchema,\
    FeatureTodo, FeatureTodoSchema,\
    FeatureNote, FeatureNoteSchema
from flask import jsonify, request, make_response
from flask_restful import Api, Resource
from flask_login import current_user, login_user

api = Api(app)

class UserAPI(Resource):
    @roles('Employee', 'Administrator')
    def get(self, id=None):
        if id is None:
            results = User.query.all()
            schema = UserSchema(many=True)
        else:
            results = User.query.get(id)
            schema = UserSchema()
        return schema.jsonify(results)

    @roles('Administrator')
    def post(self):
        schema = UserSchema()
        json_data = request.get_json()
        if not json_data:
            return jsonify({'message': 'No data provided'}), 400
        data, errors = schema.load(json_data)
        data.user_id = current_user.id
        if errors:
            return jsonify(errors), 422
        db.session.add(data)
        db.session.commit()
        result = schema.dump(Client.query.get(data.id))
        return make_response(jsonify({'message': 'Added a user.', 'user': result.data}), 201)


class ClientAPI(Resource):
    @roles('Employee', 'Administrator')
    def get(self, id=None):
        if id is None:
            results = Client.query.all()
            schema = ClientSchema(many=True)
        else:
            results = Client.query.get(id)
            schema = ClientSchema()
        return make_response(schema.jsonify(results), 200)

    @roles('Administrator')
    def post(self):
        schema = ClientSchema()
        json_data = request.get_json()
        if not json_data:
            return jsonify({'message': 'No data provided'}), 400
        data, errors = schema.load(json_data)
        data.user_id = current_user.id
        if errors:
            return jsonify(errors), 422
        db.session.add(data)
        db.session.commit()
        result = schema.dump(Client.query.get(data.id))
        return make_response(jsonify({'message': 'Added a client.', 'client': result.data}), 201)


class ClientNoteAPI(Resource):
    @roles('Employee', 'Administrator')
    def get(self, id=None):
        if id is None:
            results = ClientNote.query.all()
            schema = ClientNoteSchema(many=True)
        else:
            results = ClientNote.query.get(id)
            schema = ClientNoteSchema()
        return make_response(schema.jsonify(results), 200)

    @roles('Employee', 'Administrator')
    def post(self):
        schema = ClientNoteSchema()
        json_data = request.get_json()
        if not json_data:
            return jsonify({'message': 'No data provided'}), 400
        data, errors = schema.load(json_data)
        data.user_id = current_user.id
        if errors:
            return jsonify(errors), 422
        db.session.add(data)
        db.session.commit()
        result = schema.dump(ClientNote.query.get(data.id))
        return make_response(jsonify({'message': 'Added a client note.', 'clientnote': result.data}), 201)


class ProductAreaAPI(Resource):
    @roles('Employee', 'Administrator')
    def get(self, id=None):
        if id is None:
            results = ProductArea.query.all()
            schema = ProductAreaSchema(many=True)
        else:
            results = ProductArea.query.get(id)
            schema = ProductAreaSchema()
        return make_response(schema.jsonify(results), 200)

    @roles('Administrator')
    def post(self):
        schema = ProductAreaSchema()
        json_data = request.get_json()
        if not json_data:
            return jsonify({'message': 'No data provided'}), 400
        data, errors = schema.load(json_data)
        data.user_id = current_user.id
        if errors:
            return jsonify(errors), 422
        db.session.add(data)
        db.session.commit()
        result = schema.dump(ProductArea.query.get(data.id))
        return make_response(jsonify({'message': 'Added a product area.', 'productarea': result.data}), 201)


class FeatureAPI(Resource):
    @roles('Employee', 'Administrator')
    def get(self, id=None):
        if id is None:
            results = Feature.query.all()
            schema = FeatureSchema(many=True)
        else:
            results = Feature.query.get(id)
            schema = FeatureSchema()
        return make_response(schema.jsonify(results), 200)

    @roles('Employee', 'Administrator')
    def post(self):
        schema = FeatureSchema()
        json_data = request.get_json()
        if not json_data:
            return jsonify({'message': 'No data provided'}), 400
        data, errors = schema.load(json_data)
        data.user_id = current_user.id
        if errors:
            return jsonify(errors), 422
        db.session.add(data)
        db.session.commit()
        result = schema.dump(Feature.query.get(data.id))
        return make_response(jsonify({'message': 'Added a feature.', 'feature': result.data}), 201)


class FeatureTodoAPI(Resource):
    @roles('Employee', 'Administrator')
    def get(self, id=None):
        if id is None:
            results = FeatureTodo.query.all()
            schema = FeatureTodoSchema(many=True)
        else:
            results = FeatureTodo.query.get(id)
            schema = FeatureTodoSchema()
        return make_response(schema.jsonify(results), 200)

    @roles('Employee', 'Administrator')
    def post(self):
        schema = FeatureTodoSchema()
        json_data = request.get_json()
        if not json_data:
            return jsonify({'message': 'No data provided'}), 400
        data, errors = schema.load(json_data)
        data.user_id = current_user.id
        if errors:
            return jsonify(errors), 422
        db.session.add(data)
        db.session.commit()
        result = schema.dump(FeatureTodo.query.get(data.id))
        return make_response(jsonify({'message': 'Added a feature to-do.', 'featuretodo': result.data}), 201)


class FeatureNoteAPI(Resource):
    @roles('Employee', 'Administrator')
    def get(self, id=None):
        if id is None:
            results = FeatureNote.query.all()
            schema = FeatureNoteSchema(many=True)
        else:
            results = FeatureNote.query.get(id)
            schema = FeatureNoteSchema()
        return make_response(schema.jsonify(results), 200)

    @roles('Employee', 'Administrator')
    def post(self):
        schema = FeatureNoteSchema()
        json_data = request.get_json()
        if not json_data:
            return jsonify({'message': 'No data provided'}), 400
        data, errors = schema.load(json_data)
        data.user_id = current_user.id
        if errors:
            return jsonify(errors), 422
        db.session.add(data)
        db.session.commit()
        result = schema.dump(FeatureNote.query.get(data.id))
        return make_response(jsonify({'message': 'Added a feature note.', 'featurenote': result.data}), 201)


api.add_resource(UserAPI, '/user', '/user/<int:id>', endpoint='user')
api.add_resource(ClientAPI, '/client', '/client/<int:id>', endpoint='client')
api.add_resource(ClientNoteAPI, '/clientnote', '/clientnote/<int:id>', endpoint='clientnote')
api.add_resource(ProductAreaAPI, '/productarea', '/productarea/<int:id>', endpoint='productarea')
api.add_resource(FeatureAPI, '/feature', '/feature/<int:id>', endpoint='feature')
api.add_resource(FeatureTodoAPI, '/featuretodo', '/featuretodo/<int:id>', endpoint='featuretodo')
api.add_resource(FeatureNoteAPI, '/featurenote', '/featurenote/<int:id>', endpoint='featurenote')