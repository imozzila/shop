from flask import render_template, url_for
from shop import app

@app.route('/')
def home():
    return render_template("home.html", title="Shop")

@app.route('/basket/<int:BasketId>')
def shopping_basket(BasketId):
    basket=Basket.query().get_or_404(BasketId)
