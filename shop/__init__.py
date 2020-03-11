from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'f256182c79e170d3561f6dc8ffdd9ebd4c1a32c99df6b4e3'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://C1930597:Kys123kys123@csmysql.cs.cf.ac.uk:3306/C1930597_shop'
db = SQLAlchemy(app)

from shop import routes
