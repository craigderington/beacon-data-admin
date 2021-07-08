# Routes

"""Logged-in page routes."""
from flask import Blueprint, render_template, redirect, url_for, json, request
from flask_login import current_user, login_required, logout_user
from forms import SearchForm
from . import models


# Blueprint Configuration
main_bp = Blueprint(
    'main_bp', __name__,
    template_folder='templates',
    static_folder='static'
)


@main_bp.route('/', methods=['GET'])
@login_required
def dashboard():
    """Logged-in User Dashboard, goes to search function for now"""

    return render_template(
        "home.html",

    )

@main_bp.route("/logout")
@login_required
def logout():
    """User log-out logic."""
    logout_user()
    return redirect(url_for('auth_bp.login'))

"""
@main_bp.route("/search", methods=["GET", "POST"])
def get_search_results():
    resp = models.Dealer.query.all()
    dealers = [d.as_dict() for d in resp]
    return json.jsonify(dealers)
"""           

"""
        @app.route("/", methods=["GET", "POST"])
        @app.route("/index", methods=["GET", "POST"])
        def index():
            
            Search using auto complete from database
            :params search term, str
            :return template
            
            form1 = SearchForm(request.form)

            return render_template(
                "search.html",
                form=form1
            )


        @app.route("/search", methods=["GET", "POST"])
        def get_search_results():
            return
            
            resp = Dealer.query.all()
            dealers = [d.as_dict() for d in resp]
            return jsonify(dealers)
           
"""

      
        