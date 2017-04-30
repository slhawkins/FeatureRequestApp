import os, unittest, requests
from featurerequest import app, db
from featurerequest import apiviews
from featurerequest.models import User, Client, ClientNote, ProductArea,\
                                  Feature, FeatureTodo, FeatureNote
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
    try:
        logout_user()
        login_user(User.query.filter_by(username=username).one())
        return make_response(jsonify({'message':'Success!'}), 200)
    except:
        raise
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
        self.load_dummy_data()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        #db.drop_all()

    def load_dummy_data(self):
        # Users
        users = [
            User(username='admin', role='Administrator'),
            User(username='employee', role='Employee'),
            User(username='client', role='Client')
        ]
        for user in users:
            db.session.add(user)
        # Clients
        clients = [
            Client(name='Client A', email='contact@clienta.com', phone='1234567890', user_id=1),
            Client(name='Client B', email='contact@clientb.com', phone='1234567890', user_id=1),
            Client(name='Client C', email='contact@clientc.com', phone='1234567890', user_id=1),
            ]
        for client in clients:
            db.session.add(client)
        # Client Notes
        c_notes = [
            ClientNote(user_id=1, client_id=1, note='May be willing to start a new project with us.'),
            ClientNote(user_id=1, client_id=2, note='May be willing to start a new project with us.'),
            ClientNote(user_id=1, client_id=3, note='May be willing to start a new project with us.')
        ]
        for note in c_notes:
            db.session.add(note)
        # Product Areas
        products = [
            ProductArea(user_id=1, name='Policies', description=''),
            ProductArea(user_id=1, name='Billing', description=''),
            ProductArea(user_id=1, name='Claims', description=''),
            ProductArea(user_id=1, name='Reports', description='')
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
        # Feature To-dos
        todos = [
            FeatureTodo(user_id=1, feature_id=1, priority=1, todo='Beam me up, Scotty'),
            FeatureTodo(user_id=1, feature_id=2, priority=1, todo='Beam me up, Scotty'),
            FeatureTodo(user_id=1, feature_id=3, priority=1, todo='Beam me up, Scotty'),
            FeatureTodo(user_id=1, feature_id=4, priority=1, todo='Beam me up, Scotty'),
            FeatureTodo(user_id=1, feature_id=5, priority=1, todo='Beam me up, Scotty'),
            FeatureTodo(user_id=1, feature_id=6, priority=1, todo='Beam me up, Scotty'),
            FeatureTodo(user_id=1, feature_id=6, priority=2, todo='Now beam me back!'),
        ]
        for todo in todos:
            db.session.add(todo)
        f_notes = [
            FeatureNote(user_id=1, feature_id=1, note='We may have to upgrade the MySQL instance RAM for this.'),
            FeatureNote(user_id=1, feature_id=2, note='We may have to upgrade the MySQL instance RAM for this.'),
            FeatureNote(user_id=1, feature_id=6, note='We may have to upgrade the MySQL instance RAM for this.'),
        ]
        for note in f_notes:
            db.session.add(note)
        db.session.commit()