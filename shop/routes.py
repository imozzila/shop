from flask import render_template, url_for, redirect, jsonify, request, flash
from shop import app, db, forms, login_manager
from shop.models import Item, User, Basket, WishList
from flask_login import login_required, login_user, current_user, logout_user
from flask_admin.contrib.sqla import ModelView



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
    item = Item.query.all()
    return render_template('home.html', pages=pages, item=item, info=info, page_list=list(pages.keys()))

@app.route('/basket/')
def shopping_basket():
    contents = []
    user = load_user(current_user.UserId)
    pages = organise_pages()
    basket = Basket.query.filter_by(UserId=user.UserId)
    for entry in basket:
        item = Item.query.filter_by(ItemId=entry.ItemId).first()
        contents.append(item)
    return render_template('basket.html', pages=pages, page_list=list(pages.keys()), contents=contents)

@app.route('/wishlist/<int:itemid>/<int:mode>')
def wishlist(itemid, mode):
    pages=organise_pages()
    itemi = itemid+1
    user = load_user(current_user.UserId)
    if mode == 1:
        if itemid < db.session.query(Item).count():
            addtowishlist=WishList(UserId=user.UserId, ItemId=itemi)
            db.session.add(addtowishlist)
    if mode == 2:
        WishList.query.filter_by(UserId=user.UserId).filter_by(ItemId=itemi).delete()
    db.session.commit()
    wish = WishList.query.all()
    item = Item.query.all()
    return render_template('wishlist.html', pages=pages, wishlist=wish, item=item, page_list=list(pages.keys()))


@app.route('/checkout/<int:BasketId>')
@login_required
def checkout(BasketId):
    pages = organise_pages()
    basket=Basket.query().get_or_404(BasketId, pages=pages, page_list=list(pages.keys()))
    return render_template('checkout.html')
@app.route('/signup', methods=['GET','POST'])
def signup():
    pages = organise_pages()
    form = forms.RegisterForm()
    if form.validate_on_submit():
        new_user = User(UserName=form.username.data, UserEmail=form.email.data, UserPassword=form.password.data)
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
        print(user)
        if user:
            if user.UserPassword == form.password.data:
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

@app.route('/updateBasket', methods=["POST"])
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

@app.route('/info/<string:itemid>', methods=['GET'])
def info(itemid):
    pages = organise_pages()
    item = Item.query.all()
    return render_template('info.html', pages=pages, itemid=int(itemid)-1, item=item, page_list=list(pages.keys()))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/home')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
