"""This is the majority of the Github OAuth code, taken from the example at:
   http://flask-dance.readthedocs.io/en/latest/quickstarts/github.html
"""
from functools import wraps
from featurerequest import app, db
from featurerequest.models import User, OAuth
from flask import flash, jsonify, make_response
from flask_dance.contrib.github import make_github_blueprint, github
from flask_dance.consumer.backend.sqla import SQLAlchemyBackend
from flask_dance.consumer import oauth_authorized, oauth_error
from flask_login import LoginManager, current_user, login_user
from sqlalchemy.orm.exc import NoResultFound

# Begin setup of the blueprint
github_blueprint = make_github_blueprint(
    client_id=app.config['CLIENT_ID'],
    client_secret=app.config['CLIENT_SECRET']
)
app.register_blueprint(github_blueprint, url_prefix="/login")

# Setup login manager
login_manager = LoginManager()
login_manager.login_view = 'github.login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    """Shorthand method to load the user from the User model."""
    return User.query.get(int(user_id))

github_blueprint.backend = SQLAlchemyBackend(OAuth, db.session, user=current_user)


@oauth_authorized.connect_via(github_blueprint)
def github_logged_in(blueprint, token):
    """Login the user, create an account if one is not found."""
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
            user = User(username=username, role='Administrator')
            db.session.add(user)
            db.session.commit()
        login_user(user)
        flash("Successfully signed in with GitHub")
    else:
        msg = "Failed to fetch user info from {name}".format(name=blueprint.name)
        flash(msg, category="error")


@oauth_error.connect_via(github_blueprint)
def github_error(blueprint, error, error_description=None, error_uri=None):
    """Notifies the user when there is an OAuth provider error."""
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
    """Returns the role of the user if they're logged in, otherwise None"""
    if current_user.is_authenticated:
        return current_user.role
    return None


def roles(*allowed_roles):
    """Roles decorator from http://flask.pocoo.org/snippets/98/"""
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if get_user_role() not in allowed_roles:
                return make_response(jsonify({'message':
                                              'You do not have access to this page.'}), 403)
            return f(*args, **kwargs)
        return wrapped
    return wrapper
