"""Provides all of the views and RESTful API calls. This currently includes:
   - /logout
   - /
"""

from featurerequest import app
from featurerequest.user_auth import roles
from flask import redirect, url_for, flash, render_template
from flask_login import login_required, logout_user

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
    return render_template("home.html")