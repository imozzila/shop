from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Length, Email


class LoginForm(FlaskForm):
    username = StringField('Username:', validators=[InputRequired()])
    password = PasswordField('Password:', validators=[InputRequired()])

class RegisterForm(FlaskForm):
    email = StringField('Email:', validators=[InputRequired(), Email('Invalid Email')])
    username = StringField('Username:', validators=[InputRequired(), Length(min=5, max=20)])
    password = PasswordField('Password:', validators=[InputRequired(), Length(min=6, max=20)])
    confirm_password = PasswordField('Confirm Password:', validators=[InputRequired(), EqualTo('password', 'Passwords must match.')])
    confirm_email = StringField('Confirm Email:', validators=[InputRequired(), EqualTo('email', 'Emails must match.')])
