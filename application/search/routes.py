from flask import Blueprint, render_template, request, json
from flask import current_app as app
from forms import SearchForm
from .. import models

# Blueprint Configuration
search_bp = Blueprint(
    'search_bp', __name__,
    template_folder='templates',
    static_folder='static'
)


@search_bp.route('/search', methods=['GET'])
def search():
    
    form1 = SearchForm(request.form)

    return render_template(
        "search.html",
        form=form1
    )

@search_bp.route('/searchgo', methods=['GET','POST'])
def get_search_results():
    resp = models.Dealer.query.all()
    dealers = [d.as_dict() for d in resp]
    return json.jsonify(dealers)