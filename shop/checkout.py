from flask_wtf import FlaskForm
from wtforms.validators import InputRequired, Length, Email
from wtforms import StringField, IntegerField



class Checkout(FlaskForm):
    Firstname = StringField('First name', validators=[InputRequired()])
    Lastname = StringField('Last name', validators=[InputRequired()])
    Phonenumber = StringField('Phone number', validators=[InputRequired()])
    Postcode = StringField('Postcode', validators=[InputRequired()])
    AddressLine1 = StringField('AddressLine1', validators=[InputRequired()])
    TC = StringField('Town/City', validators=[InputRequired()])
    County = StringField('County', validators=[InputRequired()])

    Nameoncard = StringField('Name on card', validators=[InputRequired()])
    CardNumber = StringField('Card Number', validators=[InputRequired()])
    Expirydate = StringField('Expiry date', validators=[InputRequired()])
    CVV = IntegerField('CVV', validators=[InputRequired()])
