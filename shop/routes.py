from flask import render_template, url_for, redirect, jsonify, request, flash
from shop import app, db, forms, login_manager, checkout
from shop.models import Item, User, Basket, WishList
from flask_login import login_required, login_user, current_user, logout_user
from flask_bcrypt import Bcrypt, check_password_hash, generate_password_hash
from flask_admin.contrib.sqla import ModelView

bcrypt = Bcrypt(app)

def organise_pages():
    if not current_user.is_anonymous:
        user = load_user(current_user.UserId)
        print(user)
        pages = {'The Little Cheese':'home', 'Basket':'shopping_basket', user.UserName:'settings', 'Log-out':'logout'}
    else:
        pages= {'The Little Cheese':'home', 'Basket':'shopping_basket', 'Log-In':'login', 'Sign-Up':'signup'}
    return pages

@app.route('/')
@app.route('/home')
def home():
    pages = organise_pages()
    return render_template('home.html', pages=pages, page_list=list(pages.keys()))

@app.route('/basket/')
def shopping_basket():
    if not current_user.is_anonymous:
        contents = []
        user = load_user(current_user.UserId)
        pages = organise_pages()
        basket = Basket.query.filter_by(UserId=user.UserId)
        totalprice = 0
        for entry in basket:
            item = Item.query.filter_by(ItemId=entry.ItemId).first()
            totalprice += item.ItemPrice
            contents.append(item)
        return render_template('basket.html', pages=pages, page_list=list(pages.keys()), contents=contents, totalprice=totalprice)
    return 'You are not logged in. You must be logged in to view basket.'

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    pages = organise_pages()
    form = forms.Checkout()
    if form.validate_on_submit():
        return '<h1>Your order has been placed!</h1>'
    return render_template('checkout.html', form=form, pages=pages, page_list=list(pages.keys()))

@app.route('/signup', methods=['GET','POST'])
def signup():
    pages = organise_pages()
    form = forms.RegisterForm()
    if form.validate_on_submit():
        user = User.query.filter_by(UserName=form.username.data).first()
        if user:
            flash('The username already exists, please enter a different username.')
        else:
        	password_hash = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        	new_user = User(UserName=form.username.data, UserEmail=form.email.data, UserPassword=password_hash)
        	db.session.add(new_user)
        	db.session.commit()
        	return '<h1>New user has been created!</h1>'
    return render_template('signup.html', form=form, pages=pages, page_list=list(pages.keys()))

@app.route('/login', methods=['GET','POST'])
def login():
    pages = organise_pages()
    form = forms.LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(UserName=form.username.data).first()
        if user:
            if check_password_hash(user.UserPassword, form.password.data):
                login_user(user)
                return redirect(url_for('shopping_basket'))
        return '<h1>Invalid username or password.</h1>'
    return render_template('login.html', form=form, pages=pages, page_list=list(pages.keys()))

@app.route('/search', methods=["POST"])
def search():
    itemResults = []
    query = request.form.get("search", 0, type=str)
    queryResults = Item.query.filter(Item.ItemName.like(query+'%'))
    for item in queryResults:
        itemResults.append(item.ItemName)
    return jsonify(result=itemResults)

@app.route('/updateBasket/', methods=["GET","POST"])
def updateBasket():
    user = load_user(current_user.UserId)
    itemId = request.args.get('item')
    Basket.query.filter_by(UserId=user.UserId).filter_by(ItemId=itemId).delete()
    db.session.commit()
    return redirect('/basket')

@app.route('/settings')
@login_required
def settings():
    pages = organise_pages()
    return render_template('admin.html', pages=pages, page_list=list(pages.keys()))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/home')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
