from flask import Blueprint, render_template, request
from flask import current_app as app
from forms import SearchForm

# Blueprint Configuration
customer_bp = Blueprint(
    'customer_bp', __name__,
    template_folder='templates',
    static_folder='static'
)


@customer_bp.route('/customer', methods=['GET'])
def dealer():
    
    form1 = SearchForm(request.form)

    return render_template(
        "search.html",
        form=form1
    )