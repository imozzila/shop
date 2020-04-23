from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Table, Column, Integer, ForeignKey
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'f256182c79e170d3561f6dc8ffdd9ebd4c1a32c99df6b4e3'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://c1930597:Kys123kys123@csmysql.cs.cf.ac.uk:3306/c1930597_shop'
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
