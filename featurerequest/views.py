"""Provides all of the views and RESTful API calls. This currently includes:
   - /logout
   - /
"""

from featurerequest import app, db
from featurerequest.user_auth import roles
from featurerequest.models import User, Client, Product, Feature, \
                                  FeatureTodo, FeatureNote
from flask import redirect, url_for, flash, render_template
from flask_login import login_required, logout_user, current_user, login_user

@app.route("/logout")
@login_required
def logout():
    """Log the user out"""
    logout_user()
    flash("You have logged out")
    return redirect(url_for("index"))

@app.route("/")
def index():
    """Display the home page (soon to be Knockout.js app)"""
    if current_user.is_authenticated:
        return render_template("index.html")
    return render_template("home.html")

@app.route('/skipgithub')
def skipgithub():
    query = User.query.filter_by(id=1)
    user = query.one()
    login_user(user)
    return redirect('/')
    
@app.route("/resetinstance")
def populate():
    db.drop_all()
    db.create_all()
    # Users
    users = [
        User(username='admin', role='Administrator'),
        User(username='employee', role='Employee')
    ]
    for user in users:
        db.session.add(user)
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
    logout_user()
    return redirect('/')