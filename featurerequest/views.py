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
        User(username='employee', role='Employee'),
        User(username='slhawkins', role='Administrator')
    ]
    for user in users:
        db.session.add(user)
    # Clients
    clients = [
        Client(name='Client A', poc='Steve', email='steve@clienta.com', phone='1234567890', user_id=3),
        Client(name='Client B', poc='Nicole', email='nicole@clientb.com', phone='1234567890', user_id=3),
        Client(name='Client C', poc='Jess', email='jess@clientc.com', phone='1234567890', user_id=3),
        ]
    for client in clients:
        db.session.add(client)
    # Product Areas
    products = [
        Product(user_id=3, name='Policies', description='All-in-one policy administration.'),
        Product(user_id=3, name='Billing', description='Advanced billing and accounts receivable.'),
        Product(user_id=3, name='Claims', description='Manage losses from open to close.'),
        Product(user_id=3, name='Reports', description='Gain insight about your business.')
    ]
    for product in products:
        db.session.add(product)
    # Features
    features = [
        Feature(user_id=3, client_id=1, product_id=1, title='Modify Acceptance Letter', description='Client would like to modify one of the acceptance letters. The ticket URL has an example.', target_date='2017-08-10', ticket_url='http://www.example.com/', priority=1),
        Feature(user_id=3, client_id=1, product_id=2, title='Custom Invoice', description='Client would like to a custom invoice that can be readily printed on A0 paper.', target_date='2017-10-08', ticket_url='http://www.example.com', priority=2),
        Feature(user_id=3, client_id=1, product_id=3, title='Pre-populate New Field', description='Client has a new field they feel is relevent to claims and should be added to the claim automatically - too many agents have typed the field incorrectly. :-(', target_date='2018-01-31', ticket_url='http://www.example.com', priority=3),
        Feature(user_id=3, client_id=2, product_id=3, title='Alexa Voice', description='Client would like the capability to talk through various portions of a claim with Alexa.', target_date='2017-09-30', ticket_url='https://developer.amazon.com/alexa', priority=1),
        Feature(user_id=3, client_id=2, product_id=3, title='Payment Method', description='Client would like to add Bitcoin as a form of payment.', target_date='2018-01-01', ticket_url='http://www.example.com', priority=2),
        Feature(user_id=3, client_id=3, product_id=4, title='Combine Reports', description='Client would like to combine data from individual reports to make a single Network Office (NO) report.', target_date='2017-06-01', ticket_url='http://www.examplecom', priority=1)
    ]
    for feature in features:
        db.session.add(feature)
    # Feature To-dos
    todos = [
        FeatureTodo(user_id=3, feature_id=1, priority=1, todo='Beam me up, Scotty'),
        FeatureTodo(user_id=3, feature_id=2, priority=1, todo='Beam me up, Scotty'),
        FeatureTodo(user_id=3, feature_id=3, priority=1, todo='Beam me up, Scotty'),
        FeatureTodo(user_id=3, feature_id=4, priority=1, todo='Beam me up, Scotty'),
        FeatureTodo(user_id=3, feature_id=5, priority=1, todo='Beam me up, Scotty'),
        FeatureTodo(user_id=3, feature_id=6, priority=1, todo='Beam me up, Scotty'),
        FeatureTodo(user_id=3, feature_id=6, priority=2, todo='Now beam me back!'),
    ]
    for todo in todos:
        db.session.add(todo)
    f_notes = [
        FeatureNote(user_id=2, feature_id=1, note='That will likely push the letter over to a second page. Are they certain that is what they want?'),
        FeatureNote(user_id=2, feature_id=2, note='It will be difficult to make sense of any data on that big of a paper, can you verify that size font they want on it?'),
        FeatureNote(user_id=2, feature_id=3, note='We should have that data in the database already, so it will be easy to do.'),
        FeatureNote(user_id=2, feature_id=4, note='Alexa rocks! Just ask her to sing and you will see!'),
        FeatureNote(user_id=2, feature_id=5, note='There are some regulatory issues with using Bitcoin, we may not be able to do this.'),
        FeatureNote(user_id=2, feature_id=6, note='Those reports are done in SSRS, so it should be fairly easy to do.'),
    ]
    for note in f_notes:
        db.session.add(note)
    db.session.commit()
    logout_user()
    return redirect('/')