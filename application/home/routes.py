from flask import Blueprint, render_template, request
from flask import current_app as app
from forms import SearchForm


# Blueprint Configuration
home_bp = Blueprint(
    'home_bp', __name__,
    template_folder='templates',
    static_folder='static'
)


@home_bp.route('/home', methods=['GET'])
def home():
    """Homepage."""

    return render_template(
        "home.html"
    )