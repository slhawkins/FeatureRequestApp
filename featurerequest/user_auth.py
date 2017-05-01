"""This is the majority of the Github OAuth code, taken from the example at:
   http://flask-dance.readthedocs.io/en/latest/quickstarts/github.html
"""

from featurerequest import app, db
from featurerequest.models import User, OAuth
from flask import flash, jsonify, make_response
from flask_dance.contrib.github import make_github_blueprint, github
from flask_dance.consumer.backend.sqla import SQLAlchemyBackend
from flask_dance.consumer import oauth_authorized, oauth_error
from flask_login import LoginManager, current_user, login_user
from sqlalchemy.orm.exc import NoResultFound
from functools import wraps

# Begin setup of the blueprint
blueprint = make_github_blueprint(
    client_id=app.config['CLIENT_ID'],
    client_secret=app.config['CLIENT_SECRET']
)
app.register_blueprint(blueprint, url_prefix="/login")

# Setup login manager
login_manager = LoginManager()
login_manager.login_view = 'github.login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Setup SQLAlchemy backend for OAuth
blueprint.backend = SQLAlchemyBackend(OAuth, db.session, user=current_user)

# create/login local user on successful OAuth login
@oauth_authorized.connect_via(blueprint)
def github_logged_in(blueprint, token):
    if not token:
        flash("Failed to log in with {name}".format(name=blueprint.name))
        return
    # figure out who the user is
    resp = blueprint.session.get("/user")
    if resp.ok:
        username = resp.json()["login"]
        query = User.query.filter_by(username=username)
        try:
            user = query.one()
        except NoResultFound:
            # create a user
            user = User(username=username)
            db.session.add(user)
            if user.id == 1:
                user.role = 'Administrator'
            db.session.commit()
        login_user(user)
        flash("Successfully signed in with GitHub")
    else:
        msg = "Failed to fetch user info from {name}".format(name=blueprint.name)
        flash(msg, category="error")

# notify on OAuth provider error
@oauth_error.connect_via(blueprint)
def github_error(blueprint, error, error_description=None, error_uri=None):
    msg = (
        "OAuth error from {name}! "
        "error={error} description={description} uri={uri}"
    ).format(
        name=blueprint.name,
        error=error,
        description=error_description,
        uri=error_uri,
    )
    flash(msg, category="error")

def get_user_role():
    if current_user.is_authenticated:
        return current_user.role
    return None

# http://flask.pocoo.org/snippets/98/
def roles(*roles):
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if get_user_role() not in roles:
                return make_response(jsonify({'message': 'You do not have access to this page'}), 403)
            return f(*args, **kwargs)
        return wrapped
    return wrapper