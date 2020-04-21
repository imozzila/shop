from datetime import datetime
from shop import db

class Item(db.Model):
    ItemId = db.Column(db.Integer, primary_key=True, nullable=False)
    ItemName = db.Column(db.String(255), nullable=False)
    ItemPrice = db.Column(db.Integer, nullable=False)
    ItemDesc = db.Column(db.String(255))
    ItemSales = db.Column(db.Integer, nullable=False)

class User(db.Model):
    UserId = db.Column(db.Integer, primary_key=True, nullable=False)
    UserName = db.Column(db.String(255), nullable=False)
    UserPassword = db.Column(db.String(255), nullable=False)
    UserEmail = db.Column(db.String(255), nullable=False)

class Basket(db.Model):
    BasketId = db.Column(db.Integer, primary_key=True, nullable=False)
    UserId = db.Column(db.Integer, db.ForeignKey("User.UserId"), nullable=False)
    ItemId = db.Column(db.Integer, db.ForeignKey("Item.ItemId"), nullable=False)

class WishList(db.Model):
    WishListId= db.Column(db.Integer, primary_key=True, nullable=False)
    UserId = db.Column(db.Integer, db.ForeignKey("User.UserId"), nullable=False)
    ItemId = db.Column(db.Integer, db.ForeignKey("Item.ItemId"), nullable=False)
