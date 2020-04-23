from flask import render_template, url_for, redirect
from shop import app, db, forms, login_manager
from shop.models import Item, User, Basket, WishList
from flask_login import login_required, login_user, current_user

pages= {'Home':'home', 'Basket':'shopping_basket', 'Log-In':'login', 'Sign-Up':'signup'}
@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', pages=pages, page_list=list(pages.keys()))

@app.route('/basket/')
def shopping_basket():
    user = load_user(current_user.UserId)
    #basket=Basket.query().get_or_404(BasketId)
    return render_template('basket.html', pages=pages, page_list=list(pages.keys()))

@app.route('/checkout/<int:BasketId>')
@login_required
def checkout(BasketId):
    basket=Basket.query().get_or_404(BasketId, pages=pages, page_list=list(pages.keys()))

    return render_template('checkout.html')
@app.route('/signup', methods=['GET','POST'])
def signup():
    form = forms.RegisterForm()
    if form.validate_on_submit():
        new_user = User(UserName=form.username.data, UserEmail=form.email.data, UserPassword=form.password.data)
        db.session.add(new_user)
        db.session.commit()
        return '<h1>New user has been created!</h1>'
    return render_template('signup.html', form=form, pages=pages, page_list=list(pages.keys()))

@app.route('/login', methods=['GET','POST'])
def login():
    form = forms.LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(UserName=form.username.data).first()
        if user:
            if user.UserPassword == form.password.data:
                login_user(user)
                return redirect(url_for('shopping_basket'))
        return '<h1>Invalid username or password.</h1>'
    return render_template('login.html', form=form, pages=pages, page_list=list(pages.keys()))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
