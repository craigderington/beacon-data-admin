from flask import Blueprint, render_template, request
from flask import current_app as app
from forms import SearchForm

# Blueprint Configuration
dealer_bp = Blueprint(
    'dealer_bp', __name__,
    template_folder='templates',
    static_folder='static'
)


@dealer_bp.route('/dealer', methods=['GET'])
def dealer():
    form1 = SearchForm(request.form)

    return render_template(
        "search.html",
        form=form1
    )