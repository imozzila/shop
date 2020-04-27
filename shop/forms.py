from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField
from wtforms.validators import InputRequired, Length, Email


class LoginForm(FlaskForm):
    username = StringField('Username:', validators=[InputRequired()])
    password = PasswordField('Password:', validators=[InputRequired()])

class RegisterForm(FlaskForm):
    email = StringField('Email:', validators=[InputRequired(), Email('Invalid email')])
    username = StringField('Username:', validators=[InputRequired()])
    password = PasswordField('Password:', validators=[InputRequired()])

class Checkout(FlaskForm):
    Firstname = StringField('Firstname', validators=[InputRequired()])
    Lastname = StringField('Lastname', validators=[InputRequired()])
    Phonenumber = StringField('Phonenumber', validators=[InputRequired])
    Postcode = StringField('Postcode', validators=[InputRequired()])
    AddressLine1 = StringField('AddressLine1', validators=[InputRequired()])
    TC = StringField('Town/City', validators=[InputRequired()])
    County = StringField('County', validators=[InputRequired()])

    Nameoncard = StringField('Nameoncard', validators=[InputRequired()])
    CardNumber = StringField('CardNumber', validators=[InputRequired()])
    Expirydate = StringField('Expirydate', validators=[InputRequired()])
    CVV = IntegerField('CVV', validators=[InputRequired()])
