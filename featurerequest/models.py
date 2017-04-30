"""Provides all of the required models for the application. This includes:
   - User
   - OAuth
   - Client
   - ClientNote
   - ProductArea
   - Feature
   - FeatureTodo
   - FeatureNote

   Marshmallow schema's are also created to make RESTful API life easy.
"""

from datetime import datetime
from featurerequest import db, ma
from flask_dance.consumer.backend.sqla import OAuthConsumerMixin
from flask_login import UserMixin


class User(db.Model, UserMixin):
    """User table, currently only holds the username and role."""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250), unique=True, nullable=False)
    role = db.Column(db.Enum('Client', 'Employee', 'Administrator'), server_default='Client')

class UserSchema(ma.ModelSchema):
    class Meta:
        model = User


class OAuth(OAuthConsumerMixin, db.Model):
    """OAuth table, used internally by Flask-Dance for storing OAuth tokens."""
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))

    user = db.relationship(User)


class Client(db.Model):
    """Client table, allows clients to be added/updated/removed."""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    created = db.Column(db.DateTime, default=datetime.now())
    name = db.Column(db.String(250))
    email = db.Column(db.String(250))
    phone = db.Column(db.String(15))
    user = db.relationship(User)
    """
    def __init__(self, name, email, phone, user_id=None):
        self.name = name
        self.email = email
        self.phone = phone
        self.user_id = user_id
    """
    def __repr__(self):
        return '<Client {}>'.format(self.name)


class ClientSchema(ma.ModelSchema):
    class Meta:
        model = Client


class ClientNote(db.Model):
    """Client note table, users can add notes about a specific client."""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    client_id = db.Column(db.Integer, db.ForeignKey(Client.id))
    created = db.Column(db.DateTime, default=datetime.now())
    note = db.Column(db.String(500))

    user = db.relationship(User)
    client = db.relationship(Client)

class ClientNoteSchema(ma.ModelSchema):
    class Meta:
        model = ClientNote


class ProductArea(db.Model):
    """Product area's table, allows for additional product areas to be added
    aside from the default Policies, Billing, Claims, and Reports."""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    created = db.Column(db.DateTime, default=datetime.now())
    name = db.Column(db.String(50))
    description = db.Column(db.String(500))

    user = db.relationship(User)

class ProductAreaSchema(ma.ModelSchema):
    class Meta:
        model = ProductArea


class Feature(db.Model):
    """Feature table, stores each individual feature request."""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    client_id = db.Column(db.Integer, db.ForeignKey(Client.id))
    product_id = db.Column(db.Integer, db.ForeignKey(ProductArea.id))
    created = db.Column(db.DateTime, default=datetime.now())
    title = db.Column(db.String(50))
    description = db.Column(db.String(500))
    priority = db.Column(db.SmallInteger)
    target_date = db.Column(db.DateTime)
    ticket_url = db.Column(db.String(2000))

    user = db.relationship(User)
    client = db.relationship(Client)
    project = db.relationship(ProductArea)

class FeatureSchema(ma.ModelSchema):
    class Meta:
        model = Feature


class FeatureTodo(db.Model):
    """Feature to-do table, to-do's can be added to a feature."""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    feature_id = db.Column(db.Integer, db.ForeignKey(Feature.id))
    created = db.Column(db.DateTime, default=datetime.now())
    priority = db.Column(db.SmallInteger)
    todo = db.Column(db.String(250))
    completed = db.Column(db.Boolean, default=False)

    feature = db.relationship(Feature)
    user = db.relationship(User)

class FeatureTodoSchema(ma.ModelSchema):
    class Meta:
        model = FeatureTodo

class FeatureNote(db.Model):
    """Feature note table, allows for thread-like discussion about a feature."""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    feature_id = db.Column(db.Integer, db.ForeignKey(Feature.id))
    created = db.Column(db.DateTime, default=datetime.now())
    note = db.Column(db.String(500))

    feature = db.relationship(Feature)
    user = db.relationship(User)

class FeatureNoteSchema(ma.ModelSchema):
    class Meta:
        model = FeatureNote
