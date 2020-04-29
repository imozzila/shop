from flask import render_template, url_for, redirect, jsonify, request, flash

from shop import app, db, forms, login_manager, admin, basic_auth
from shop.models import Item, User, Basket, WishList, OrderHistory
from flask_login import login_required, login_user, current_user, logout_user
from flask_bcrypt import Bcrypt, check_password_hash, generate_password_hash
from flask_admin.contrib.sqla import ModelView

bcrypt = Bcrypt(app)

def organise_pages():
    if not current_user.is_anonymous:
        countries = []
        types = []
        for country in db.session.query(Item.ItemCountry).distinct():
            countries.append(country)
        for type in db.session.query(Item.ItemType).distinct():
            types.append(type)
        user = load_user(current_user.UserId)
        print(user)
        pages = {'Home':'home', 'Basket':'shopping_basket', 'Admin':'settings', 'Log-out':'logout'}
    else:
        pages= {'Home':'home', 'Basket':'shopping_basket', 'Log-In':'login', 'Sign-Up':'signup'}
    return pages, countries, types

@app.route('/')
@app.route('/home')
def home():

    pages, countries, types = organise_pages()
    item = Item.query.all()
    return render_template('home.html', pages=pages, item=item, countries=countries, types=types, info=info, page_list=list(pages.keys()))

@app.route('/basket/')
def shopping_basket():
    countries = []
    types = []
    pages=organise_pages()
    for country in db.session.query(Item.ItemCountry).distinct():
        countries.append(country)
    for type in db.session.query(Item.ItemType).distinct():
        types.append(type)
        contents = []
    if not current_user.is_anonymous:
        user = load_user(current_user.UserId)

        basket = Basket.query.filter_by(UserId=user.UserId)
        totalprice = 0
        for entry in basket:
            item = Item.query.filter_by(ItemId=entry.ItemId).first()
            totalprice += item.ItemPrice
            contents.append(item)
        return render_template('basket.html', pages=pages, page_list=list(pages.keys()), contents=contents, totalprice=totalprice)
    return redirect('error')


@app.route('/wishlist/<int:itemid>/<int:mode>')
def wishlist(itemid, mode):
    wishlistids = []

    already = ""

    pages, countries, types=organise_pages()
    itemi = itemid+1
    user = load_user(current_user.UserId)
    items = WishList.query.all()
    for item in items:
        wishlistids.append(item.ItemId)
    if mode == 1:
        if itemi not in wishlistids:
            if itemid < db.session.query(Item).count():
                addtowishlist=WishList(UserId=user.UserId, ItemId=itemi)
                db.session.add(addtowishlist)
        else:
            already = "This item is already in the wishlist!"
    if mode == 2:
        WishList.query.filter_by(UserId=user.UserId).filter_by(ItemId=itemi).delete()
    db.session.commit()
    wish = WishList.query.all()
    item = Item.query.all()
    return render_template('wishlist.html', pages=pages, wishlist=wish, already=already, item=item, countries=countries, types=types, page_list=list(pages.keys()))


@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    countries = []
    types = []
    for country in db.session.query(Item.ItemCountry).distinct():
        countries.append(country)
    for type in db.session.query(Item.ItemType).distinct():
        types.append(type)
    pages = organise_pages()
    form = forms.Checkout()
    if form.validate_on_submit():
        return '<h1>Your order has been placed!</h1>'
    return render_template('checkout.html', form=form, countries=countries, types=types, pages=pages, page_list=list(pages.keys()))

@app.route('/delete', methods=['GET','POST'])
def delete():
    countries = []
    types = []
    for country in db.session.query(Item.ItemCountry).distinct():
        countries.append(country)
    for type in db.session.query(Item.ItemType).distinct():
        types.append(type)
    pages=organise_pages()
    form = forms.DeleteForm()
    if form.validate_on_submit():
        user = User.query.filter_by(UserName=form.username.data).first()
        if user:
            if check_password_hash(user.UserPassword, form.password.data):
                db.session.delete(user)
                db.session.commit()
                return '<h1>Your account has been deleted.</h1>'
        return '<h1>Invalid username or password.</h1>'
    return render_template('delete.html', form=form, countries=countries, types=types, pages=pages, page_list=list(pages.keys()))


@app.route('/signup', methods=['GET','POST'])
def signup():
    countries = []
    types = []
    for country in db.session.query(Item.ItemCountry).distinct():
        countries.append(country)
    for type in db.session.query(Item.ItemType).distinct():
        types.append(type)
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
    return render_template('signup.html', form=form, pages=pages, countries=countries, types=types, page_list=list(pages.keys()))

@app.route('/login', methods=['GET','POST'])
def login():
    countries = []
    types = []
    for country in db.session.query(Item.ItemCountry).distinct():
        countries.append(country)
    for type in db.session.query(Item.ItemType).distinct():
        types.append(type)
    pages = organise_pages()
    form = forms.LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(UserName=form.username.data).first()
        if user:
            if check_password_hash(user.UserPassword, form.password.data):
                login_user(user)
                return redirect(url_for('shopping_basket'))
        return '<h1>Invalid username or password.</h1>'
    return render_template('login.html', form=form, pages=pages, countries=countries, types=types, page_list=list(pages.keys()))

@app.route('/search', methods=["POST"])
def search():
    itemResults = []
    query = request.form.get("search", 0, type=str)
    queryResults = Item.query.filter(Item.ItemName.like(query+'%'))
    for item in queryResults:
        itemResults.append(item.ItemName)
    return jsonify(result=itemResults)

@app.route('/updateBasket', methods=["POST"])
def updateBasket():
    user = load_user(current_user.UserId)
    itemId = request.args.get('item')
    Basket.query.filter_by(UserId=user.UserId).filter_by(ItemId=itemId).delete()
    db.session.commit()
    return redirect('/basket')


@app.route('/itemlist/<string:search>/<int:mode>')
def itemlist(search, mode):
    pages = organise_pages()
    contents = []
    countries = []
    types = []
    for country in db.session.query(Item.ItemCountry).distinct():
        countries.append(country)
    for type in db.session.query(Item.ItemType).distinct():
        types.append(type)
    items = Item.query.all()
    if mode == 1:
        for item in items:
            if item.ItemType == search:
                contents.append(item)
    if mode == 2:
        for item in items:
            if item.ItemCountry == search:
                contents.append(item)
    if mode == 3:
        for item in items:
            contents.append(item)

    return render_template('itemlist.html', pages=pages, types=types, contents=contents, countries=countries, page_list=list(pages.keys()))

@app.route('/settings')
@login_required
@basic_auth.required
def settings():
    pages = organise_pages()
    return redirect(url_for('user.index_view'))

@app.route('/info/<string:itemid>', methods=['GET'])
def info(itemid):
    countries = []
    types = []
    for country in db.session.query(Item.ItemCountry).distinct():
        countries.append(country)
    for type in db.session.query(Item.ItemType).distinct():
        types.append(type)
    pages = organise_pages()
    item = Item.query.all()
    return render_template('info.html', pages=pages, countries=countries, types=types, itemid=int(itemid)-1, item=item, page_list=list(pages.keys()))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/home')

@app.route('/error')
def error():
    pages=organise_pages()

    return render_template('error.html', pages=pages, page_list=list(pages.keys()))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Item, db.session))
admin.add_view(ModelView(Basket, db.session))
admin.add_view(ModelView(WishList, db.session))
admin.add_view(ModelView(OrderHistory, db.session))
