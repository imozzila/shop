from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = '<paste SECRET_KEY here>'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://C1930597:Kys123kys123@csmysql.cs.cf.ac.uk:3306/C1930597_shop'
from shop import routes
