from flask import Blueprint, render_template, request
from flask import current_app as app
from forms import SearchForm


# Blueprint Configuration
home_bp = Blueprint(
    'home_bp', __name__,
    template_folder='templates',
    static_folder='static'
)


@home_bp.route('/search', methods=['GET'])
def home():
    """Homepage."""
    form1 = SearchForm(request.form)

    return render_template(
        "search.html",
        form=form1
    )