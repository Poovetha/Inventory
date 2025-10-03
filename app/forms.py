from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length, Optional, NumberRange


class ProductForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=120)])
    description = TextAreaField('Description', validators=[Optional(), Length(max=255)])
    submit = SubmitField('Save')


class LocationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=120)])
    address = TextAreaField('Address', validators=[Optional(), Length(max=255)])
    submit = SubmitField('Save')


class MovementForm(FlaskForm):
    movement_id = StringField('Movement ID', validators=[DataRequired(), Length(max=64)])
    product_id = SelectField('Product', validators=[DataRequired()])
    from_location = SelectField('From Location', validators=[Optional()])
    to_location = SelectField('To Location', validators=[Optional()])
    qty = IntegerField('Quantity', validators=[DataRequired(), NumberRange(min=1)])
    submit = SubmitField('Save')
