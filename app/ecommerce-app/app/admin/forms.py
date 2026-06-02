"""
Admin forms for product and category management
"""
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FloatField, IntegerField, SelectField, SubmitField
from wtforms.validators import DataRequired, NumberRange, Length, URL, Optional

class ProductForm(FlaskForm):
    name = StringField('Product Name', validators=[
        DataRequired(),
        Length(min=1, max=200)
    ])
    description = TextAreaField('Description', validators=[Length(max=1000)])
    price = FloatField('Price', validators=[
        DataRequired(),
        NumberRange(min=0.01, message='Price must be greater than 0')
    ])
    stock = IntegerField('Stock Quantity', validators=[
        DataRequired(),
        NumberRange(min=0, message='Stock cannot be negative')
    ])
    category_id = SelectField('Category', coerce=int, validators=[DataRequired()])
    image_url = StringField('Image URL', validators=[
        Optional(),
        URL(message='Please enter a valid URL'),
        Length(max=500)
    ])
    submit = SubmitField('Save Product')

class CategoryForm(FlaskForm):
    name = StringField('Category Name', validators=[
        DataRequired(),
        Length(min=1, max=100)
    ])
    description = TextAreaField('Description', validators=[Length(max=500)])
    submit = SubmitField('Save Category')