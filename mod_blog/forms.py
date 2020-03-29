from flask_wtf import FlaskForm
from wtforms import TextField, TextAreaField, SelectMultipleField
from wtforms.validators import DataRequired
from utils.forms import MultipleCheckBoxField

class PostForm(FlaskForm):
    title = TextField(validators=[DataRequired()])
    summary = TextAreaField()
    content = TextAreaField(validators=[DataRequired()])
    slug = TextField(validators=[DataRequired()])
    
    # [METHOD 1]
    # categories = SelectMultipleField(choices=[])
    # categories = SelectMultipleField(choices=[(1, "First"), (2, "Secound")])
    # choices fields : 1:value 2:label
    
    # [METHOD 2]
    categories = MultipleCheckBoxField(coerce=int) # coerce is data that was selected.

class CategoryForm(FlaskForm):
    name = TextField(validators=[DataRequired()])
    slug = TextField(validators=[DataRequired()])
    description = TextAreaField()

class SearchForm(FlaskForm):
    search_query = TextField(validators=[DataRequired()])