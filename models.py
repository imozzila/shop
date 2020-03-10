from datetime import datetime
from shop import db

class Item(db.Model):
    ItemId = db.Column(db.Integer, primary_key=True, nullable=False)
    ItemName = db.Column(db.String(255), nullable=False)
    ItemPrice = db.Column(db.Integer)

class User(db.Model):
    UserId = db.Column(db.Integer, primary_key=True, nullable=False)
    UserName = db.Column(db.String(255), nullable=False)
    UserPassword = db.Column(db.String(255), nullable=False)
    UserEmail = db.Column(db.string(255), nullable=False)

class Basket(db.Model):
    BasketId = db.Column(db.Integer, primary_key=True, nullable=False)
    UserId = db.Column(db.Integer, ForeignKey("User.UserId"), nullable=False)
    ItemId = db.Column(db.Integer, ForeignKey("Item.ItemId"), nullable=False)
