from datetime import datetime
from flask_login import UserMixin
from .extension import db, login_manager

class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)

    orders = db.relationship("Order", backref='user', lazy=True)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Books(db.Model):
    __tablename__ = "books"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, default=0)
    image = db.Column(db.String(300))

    order_items = db.relationship('OrderItem', backref='book', lazy=True)

class Order(db.Model):
        __tablename__ = "orders"

        id = db.Column(db.Integer, primary_key=True)
        user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
        total_amount = db.Column(db.Float, nullable=False)
        payment_method = db.Column(db.String(50), default='COD')
        status = db.Column(db.DateTime, default=datetime.utcnow)

        items = db.relationship("Order_Item", backref='order', lazy=True)

class Order_Item(db.Model):
     __tablename__ = "order_items"
     id = db.Column(db.Integer, primary_key=True)
     order_id = db.Column(db.Integer, db.ForeignKey("orders.id"), nullable=False)
     book_id = db.Column(db.Integer, db.ForeignKey("books.id"), nullable=False)
     quantity = db.Column(db.Integer, nullable=False)
     price = db.Column(db.Float, nullable=False)
     
