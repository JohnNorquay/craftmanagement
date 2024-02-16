from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, DateTimeField, IntegerField, FloatField, SelectField
from wtforms.validators import InputRequired, Length, EqualTo, DataRequired, Optional

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=20)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80)])
    confirm_password = PasswordField('Confirm Password', validators=[InputRequired(), EqualTo('password')])
    submit = SubmitField('Register')  # Add this line for the submit button

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=20)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('Remember Me')  # Add this line
    submit = SubmitField('Login')

class CraftProjectForm(FlaskForm):
    name = StringField('Project Name', validators=[DataRequired()])
    description = TextAreaField('Project Description')
    start_date = DateTimeField('Start Date', format='%m-%d-%Y', validators=[DataRequired()])
    end_date = DateTimeField('End Date', format='%m-%d-%Y')
    submit = SubmitField('Create Project')

class ProductForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    quantity = IntegerField('Quantity', validators=[DataRequired()])
    price = FloatField('Price', validators=[Optional()])  # Optional
    status = SelectField('Status', choices=[('Needed', 'Needed'), ('Purchased', 'Purchased')])
    submit = SubmitField('Submit')

