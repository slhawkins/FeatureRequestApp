""" Initial starting point was taken from:
       http://flask-dance.readthedocs.io/en/latest/quickstarts/github.html
"""

import sys
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

# Begin setting up Flask
app = Flask(__name__)
app.config.from_object('config')

# Setup SQLAlchemy and Marshmallow
db = SQLAlchemy(app)
ma = Marshmallow(app)

# Import/Setup user authentication and views
from featurerequest import user_auth
from featurerequest import views
from featurerequest import apiviews
