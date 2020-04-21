from flask import render_template, url_for, redirect
from shop import app
from shop import forms
from shop.models import Item, User, Basket, WishList, db

@app.route('/')
def home():
    return render_template("home.html", title="Shop")

@app.route('/basket/<int:BasketId>')
def shopping_basket(BasketId):
    basket=Basket.query().get_or_404(BasketId)

@app.route('/checkout/<int:BasketId>')
def checkout(BasketId):
    basket=Basket.query().get_or_404(BasketId)

@app.route('/signup', methods=['GET','POST'])
def signup():
    form = forms.RegisterForm()
    if form.validate_on_submit():
        new_user = User(UserName=form.username.data, UserEmail=form.email.data, UserPassword=form.password.data)
        db.session.add(new_user)
        db.session.commit()
        return '<h1>New user has been created!</h1>'
    return render_template('signup.html', form=form)

@app.route('/login', methods=['GET','POST'])
def login():
    form = forms.LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(UserName=form.username.data).first()
        if user:
            if user.UserPassword == form.password.data:
                return redirect(url_for('dashboard'))
        return '<h1>Invalid username or password.</h1>'
    return render_template('login.html', form=form)

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')
