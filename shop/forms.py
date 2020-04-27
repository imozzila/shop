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

