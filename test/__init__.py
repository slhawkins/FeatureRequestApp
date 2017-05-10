import os, unittest, requests
from featurerequest import app, db
from featurerequest import apiviews
from featurerequest.models import User, Client, Product, Feature, FeatureComment
from flask import make_response, jsonify
from flask_testing import TestCase
from flask_login import current_user, login_user, logout_user
from sqlalchemy.orm.exc import NoResultFound


# Customize app for testing. My method creates a custom route that logs in a 
# client, employee, or admin so I can do appropriate testing. For obvious reason
# this wouldn't be good to have in the main code. However, I should look at what
# I could do to use different configuration classes for testing/dev/prod. It's 
# very possible I can enable certain routes only for the testing environment.
def login_test_user(username):
    logout_user()
    if username != 'noone':
        user = User.query.filter_by(username=username).one()
        login_user(user)
    return make_response(jsonify({'message':'Success!'}), 200)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///temp.db'
app.config['TESTING'] = True
app.config['DEBUG'] = False
app.add_url_rule('/login_test/<username>', 'login_test', login_test_user)

class MyTest(TestCase):
    def create_app(self):
        return app
    
    def setUp(self):
        self.db = db
        db.drop_all()
        db.create_all()
        self.insert_users()
        self.load_dummy_data()
        self.client = self.app.test_client()
        # Variables used in test methods
        self.user_responses = {}
        self.resource_url = ''
        self.client.get('/login_test/admin')

    def tearDown(self):
        db.session.remove()
        #db.drop_all()

    def insert_users(self):
        users = [
            User(username='admin', role='Administrator'),
            User(username='employee', role='Employee')
        ]
        for user in users:
            db.session.add(user)

    def load_dummy_data(self):
        # Clients
        clients = [
            Client(name='Client A', poc='Steve', email='steve@clienta.com', phone='1234567890', user_id=1),
            Client(name='Client B', poc='Nicole', email='nicole@clientb.com', phone='1234567890', user_id=1),
            Client(name='Client C', poc='Jess', email='jess@clientc.com', phone='1234567890', user_id=1),
            ]
        for client in clients:
            db.session.add(client)
        # Product Areas
        products = [
            Product(user_id=1, name='Policies', description=''),
            Product(user_id=1, name='Billing', description=''),
            Product(user_id=1, name='Claims', description=''),
            Product(user_id=1, name='Reports', description='')
        ]
        for product in products:
            db.session.add(product)
        # Features
        features = [
            Feature(user_id=1, client_id=1, product_id=1, title='Test Feature 1', description='', priority=1),
            Feature(user_id=1, client_id=1, product_id=2, title='Test Feature 2', description='', priority=2),
            Feature(user_id=1, client_id=1, product_id=3, title='Test Feature 3', description='', priority=3),
            Feature(user_id=1, client_id=2, product_id=1, title='Test Feature 1', description='', priority=1),
            Feature(user_id=1, client_id=2, product_id=2, title='Test Feature 2', description='', priority=2),
            Feature(user_id=1, client_id=3, product_id=4, title='Test Feature', description='', priority=1),
        ]
        for feature in features:
            db.session.add(feature)
        f_notes = [
            FeatureComment(user_id=1, feature_id=1, note='We may have to upgrade the MySQL instance RAM for this.'),
            FeatureComment(user_id=1, feature_id=2, note='We may have to upgrade the MySQL instance RAM for this.'),
            FeatureComment(user_id=1, feature_id=6, note='We may have to upgrade the MySQL instance RAM for this.'),
        ]
        for note in f_notes:
            db.session.add(note)
        db.session.commit()

    def permission_helper(self):
        if not self.user_responses or not self.base_url:
            raise ValueError('The variable user_responses is not set, please set it!')
        for user in self.user_responses:
            self.client.get('/login_test/' + user)
            response = self.client.get(self.base_url)
            assert response.status_code == self.user_responses[user]['get']
            response = self.client.post(self.base_url)
            assert response.status_code == self.user_responses[user]['post']
            response = self.client.put(self.base_url)
            assert response.status_code == self.user_responses[user]['put']
            response = self.client.delete(self.base_url)
            assert response.status_code == self.user_responses[user]['delete']