from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField
from wtforms.validators import InputRequired, Length, Email, EqualTo



class LoginForm(FlaskForm):
    username = StringField('Username:', validators=[InputRequired()])
    password = PasswordField('Password:', validators=[InputRequired()])

class RegisterForm(FlaskForm):
    email = StringField('Email:', validators=[InputRequired(), Email('Invalid Email')])
    username = StringField('Username:', validators=[InputRequired(), Length(min=5, max=20)])
    password = PasswordField('Password:', validators=[InputRequired(), Length(min=6, max=20)])
    confirm_password = PasswordField('Confirm Password:', validators=[InputRequired(), EqualTo('password', 'Passwords must match.')])
    confirm_email = StringField('Confirm Email:', validators=[InputRequired(), EqualTo('email', 'Emails must match.')])

class Checkout(FlaskForm):
    Firstname = StringField('First Name', validators=[InputRequired()])
    Lastname = StringField('Last Name', validators=[InputRequired()])
    Phonenumber = StringField('Phone Number', validators=[InputRequired()])
    AddressLine1 = StringField('Address Line 1', validators=[InputRequired()])
    Postcode = StringField('Postcode', validators=[InputRequired()])
    TC = StringField('Town/City', validators=[InputRequired()])
    County = StringField('County', validators=[InputRequired()])

    Nameoncard = StringField('Name On card', validators=[InputRequired()])
    CardNumber = StringField('Card Number', validators=[InputRequired()])
    Expirydate = StringField('Expiry Date', validators=[InputRequired()])
    CVV = IntegerField('CVV', validators=[InputRequired()])
