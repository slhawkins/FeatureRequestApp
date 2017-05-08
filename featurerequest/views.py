"""Provides all of the views and RESTful API calls. This currently includes:
   - /logout
   - /
"""

from featurerequest import app, db
from featurerequest.models import User, Client, Product, Feature, FeatureComment
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
    """Bypasses Github authentication and logs them in as an administrator. I allow this since
    this application is purely for testing my abilities.
    """
    query = User.query.filter_by(id=1)
    user = query.one()
    login_user(user)
    return redirect('/')

@app.route("/resetinstance")
def resetinstance():
    """Resets the database to a stock set of data."""
    db.drop_all()
    db.create_all()
    # Users
    users = [
        User(username='admin', role='Administrator'),
        User(username='employee', role='Employee'),
        User(username='slhawkins', role='Administrator')
    ]
    for user in users:
        db.session.add(user) # pylint: disable=no-member
    # Clients
    clients = [
        Client(name='Client A', poc='Steve', email='steve@clienta.com', phone='1234567890',
               user_id=3),
        Client(name='Client B', poc='Nicole', email='nicole@clientb.com', phone='1234567890',
               user_id=3),
        Client(name='Client C', poc='Jess', email='jess@clientc.com', phone='1234567890',
               user_id=3),
        ]
    for client in clients:
        db.session.add(client) # pylint: disable=no-member
    # Product Areas
    products = [
        Product(user_id=3, name='Policies', description='All-in-one policy administration.'),
        Product(user_id=3, name='Billing',
                description='Advanced billing and accounts receivable.'),
        Product(user_id=3, name='Claims', description='Manage losses from open to close.'),
        Product(user_id=3, name='Reports', description='Gain insight about your business.')
    ]
    for product in products:
        db.session.add(product) # pylint: disable=no-member
    # Features
    features = [
        Feature(user_id=3, client_id=1, product_id=1, title='Modify Acceptance Letter',
                description='Client would like to modify one of the acceptance letters. The '\
                    'ticket URL has an example.',
                target_date='2017-08-10', ticket_url='http://www.example.com/', priority=1),
        Feature(user_id=3, client_id=1, product_id=2, title='Custom Invoice',
                description='Client would like to a custom invoice that can be readily printed '\
                    'on A0 paper.',
                target_date='2017-10-08', ticket_url='http://www.example.com', priority=2),
        Feature(user_id=3, client_id=1, product_id=3, title='Pre-populate New Field',
                description='Client has a new field they feel is relevant to claims and should '\
                    'be added to the claim automatically - too many agents have typed the field '\
                    'incorrectly. :-(',
                target_date='2018-01-31', ticket_url='http://www.example.com', priority=3),
        Feature(user_id=3, client_id=1, product_id=2, title='Hybrid Billing Automation',
                description='Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do '\
                    'eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad '\
                    'minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex '\
                    'ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate '\
                    'velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat '\
                    'cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id '\
                    'est laborum.',
                target_date='2018-02-15', ticket_url='http://www.examplecom', priority=4),
        Feature(user_id=3, client_id=1, product_id=4, title='Report Export Format',
                description='Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do '\
                    'eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad '\
                    'minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex '\
                    'ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate '\
                    'velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat '\
                    'cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id '\
                    'est laborum.',
                target_date='2018-03-01', ticket_url='http://www.examplecom', priority=5),
        Feature(user_id=3, client_id=2, product_id=3, title='Alexa Voice',
                description='Client would like the capability to talk through various portions '\
                    'of a claim with Alexa.',
                target_date='2017-09-30', ticket_url='https://developer.amazon.com/alexa',
                priority=1),
        Feature(user_id=3, client_id=2, product_id=3, title='Payment Method',
                description='Client would like to add Bitcoin as a form of payment.',
                target_date='2018-01-01', ticket_url='http://www.example.com', priority=2),
        Feature(user_id=3, client_id=2, product_id=1, title='Change Endorsement Logs',
                description='Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do '\
                    'eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad '\
                    'minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex '\
                    'ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate '\
                    'velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat '\
                    'cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id '\
                    'est laborum.',
                target_date='2018-02-01', ticket_url='http://www.examplecom', priority=3),
        Feature(user_id=3, client_id=2, product_id=4, title='Add Field',
                description='Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do '\
                    'eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad '\
                    'minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex '\
                    'ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate '\
                    'velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat '\
                    'cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id '\
                    'est laborum.',
                ticket_url='http://www.examplecom', priority=4),
        Feature(user_id=3, client_id=3, product_id=4, title='Combine Reports',
                description='Client would like to combine data from individual reports to make '\
                    'a single Network Office (NO) report.',
                target_date='2017-06-01', ticket_url='http://www.examplecom', priority=1),
        Feature(user_id=3, client_id=3, product_id=4, title='Custom Report',
                description='Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do '\
                    'eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad '\
                    'minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex '\
                    'ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate '\
                    'velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat '\
                    'cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id '\
                    'est laborum.',
                target_date='2017-10-15', ticket_url='http://www.examplecom', priority=2),
        Feature(user_id=3, client_id=3, product_id=3, title='Legal Expense Changes',
                description='Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do '\
                    'eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad '\
                    'minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex '\
                    'ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate '\
                    'velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat '\
                    'cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id '\
                    'est laborum.',
                target_date='2018-01-01', ticket_url='http://www.examplecom', priority=3),
        Feature(user_id=3, client_id=3, product_id=1, title='Reserve Calculation',
                description='Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do '\
                    'eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad '\
                    'minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex '\
                    'ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate '\
                    'velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat '\
                    'cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id '\
                    'est laborum.',
                target_date='2018-05-01', ticket_url='http://www.examplecom', priority=4)
    ]
    for feature in features:
        db.session.add(feature) # pylint: disable=no-member
    f_notes = [
        FeatureComment(user_id=2, feature_id=1, note='That will likely push the letter over to a '\
            'second page. Are they certain that is what they want?'),
        FeatureComment(user_id=2, feature_id=2, note='It will be difficult to make sense of any '\
            'data on that big of a paper, can you verify that size font they want on it?'),
        FeatureComment(user_id=2, feature_id=3, note='We should have that data in the database '\
            'already, so it will be easy to do.'),
        FeatureComment(user_id=2, feature_id=4, note='Alexa rocks! Just ask her to sing and you '\
            'will see!'),
        FeatureComment(user_id=2, feature_id=5, note='There are some regulatory issues with '\
            'using Bitcoin, we may not be able to do this.'),
        FeatureComment(user_id=2, feature_id=6, note='Those reports are done in SSRS, so it '\
            'should be fairly easy to do.'),
    ]
    for note in f_notes:
        db.session.add(note) # pylint: disable=no-member
    db.session.commit() # pylint: disable=no-member
    logout_user()
    return redirect('/')
