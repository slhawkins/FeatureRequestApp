"""Provides all of the required models and schemas for the application. This includes:
   - User/UserSchema
   - OAuth
   - Client/ClientSchema
   - Product/ProductSchema
   - Feature/FeatureSchema
   - FeatureComment/FeatureCommentSchema
"""

from datetime import datetime
from featurerequest import db, ma
from flask_dance.consumer.backend.sqla import OAuthConsumerMixin
from flask_login import UserMixin
from marshmallow import fields


class User(db.Model, UserMixin):
    """User table, holds the username and role."""
    id = db.Column(db.Integer, primary_key=True) # pylint: disable=invalid-name
    username = db.Column(db.String(250), unique=True, nullable=False)
    role = db.Column(db.Enum('Inactive', 'Employee', 'Administrator'))


class UserSchema(ma.ModelSchema):
    """Provides serialization and deserialization methods for the User model."""
    class Meta: # pylint: disable=too-few-public-methods
        """Populates the schema with properties from the SQL-Alchemy model."""
        model = User


class OAuth(OAuthConsumerMixin, db.Model): # pylint: disable=too-few-public-methods
    """OAuth table, used internally by Flask-Dance for storing OAuth tokens."""
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    user = db.relationship(User)


class Client(db.Model): # pylint: disable=too-few-public-methods
    """Client table, allows clients to be added/updated/removed."""
    id = db.Column(db.Integer, primary_key=True) # pylint: disable=invalid-name
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    created = db.Column(db.DateTime, default=lambda: str(datetime.now()))
    name = db.Column(db.String(250))
    poc = db.Column(db.String(250))
    email = db.Column(db.String(250))
    phone = db.Column(db.String(15))
    user = db.relationship(User)


class ClientSchema(ma.ModelSchema):
    """Provides serialization and deserialization methods for the Client model."""
    user = fields.Nested(UserSchema, only='username')
    class Meta: # pylint: disable=too-few-public-methods
        """Populates the schema with properties from the SQL-Alchemy model."""
        model = Client
        include_fk = True


class Product(db.Model): # pylint: disable=too-few-public-methods
    """Product area's table, allows for additional product areas to be added
    aside from the default Policies, Billing, Claims, and Reports."""
    id = db.Column(db.Integer, primary_key=True) # pylint: disable=invalid-name
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    created = db.Column(db.DateTime, default=lambda: str(datetime.now()))
    name = db.Column(db.String(50))
    active = db.Column(db.Boolean, default=True)
    description = db.Column(db.String(500))
    user = db.relationship(User)


class ProductSchema(ma.ModelSchema):
    """Provides serialization and deserialization methods for the Product model."""
    user = fields.Nested(UserSchema, only='username')
    class Meta: # pylint: disable=too-few-public-methods
        """Populates the schema with properties from the SQL-Alchemy model."""
        model = Product
        include_fk = True


class Feature(db.Model): # pylint: disable=too-few-public-methods
    """Feature table, stores each individual feature request."""
    id = db.Column(db.Integer, primary_key=True) # pylint: disable=invalid-name
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    client_id = db.Column(db.Integer, db.ForeignKey(Client.id))
    product_id = db.Column(db.Integer, db.ForeignKey(Product.id))
    created = db.Column(db.DateTime, default=lambda: str(datetime.now()))
    title = db.Column(db.String(50))
    description = db.Column(db.String(500))
    priority = db.Column(db.SmallInteger)
    target_date = db.Column(db.Date)
    ticket_url = db.Column(db.String(2000))
    user = db.relationship(User)
    client = db.relationship(Client)
    product_area = db.relationship(Product)


class FeatureSchema(ma.ModelSchema):
    """Provides serialization and deserialization methods for the Feature model."""
    user = fields.Nested(UserSchema, only='username')
    client = fields.Nested(ClientSchema, only='name')
    product_area = fields.Nested(ProductSchema, only='name')
    class Meta: # pylint: disable=too-few-public-methods
        """Populates the schema with properties from the SQL-Alchemy model."""
        model = Feature
        include_fk = True


class FeatureComment(db.Model): # pylint: disable=too-few-public-methods
    """Feature note table, allows for thread-like discussion about a feature."""
    id = db.Column(db.Integer, primary_key=True) # pylint: disable=invalid-name
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    feature_id = db.Column(db.Integer, db.ForeignKey(Feature.id))
    created = db.Column(db.DateTime, default=lambda: str(datetime.now()))
    note = db.Column(db.String(500))
    user = db.relationship(User)
    feature = db.relationship(Feature, cascade='delete')


class FeatureCommentSchema(ma.ModelSchema):
    """Provides serialization and deserialization methods for the FeatureComment model."""
    user = fields.Nested(UserSchema, only='username')
    class Meta: # pylint: disable=too-few-public-methods
        """Populates the schema with properties from the SQL-Alchemy model."""
        model = FeatureComment
        include_fk = True
