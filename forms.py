from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Length

class SearchForm(FlaskForm):
    name = StringField('name', validators=[DataRequired(), Length(max=20)], render_kw={"placeholder": "name"})