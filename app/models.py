from datetime import datetime
from flask_login import UserMixin
from .extension import db, login_manager

class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

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
    image = db.Column(db.String(300), nullable=False)

    order_items = db.relationship('Order_Item', backref='book', lazy=True)

class Order(db.Model):
        __tablename__ = "orders"

        id = db.Column(db.Integer, primary_key=True)
        user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

        first_name = db.Column(db.String(100), nullable=False)
        last_name = db.Column(db.String(100), nullable=False)
        country = db.Column(db.String(100), nullable=False)
        street_address = db.Column(db.String(250), nullable=False)
        appartment = db.Column(db.String(250), nullable=True)
        city = db.Column(db.String(100), nullable=False)
        state = db.Column(db.String(100), nullable=False)
        phone = db.Column(db.String(20), nullable=False)
        email = db.Column(db.String(100), nullable=False)

        sub_total = db.Column(db.Float, nullable=False)
        shipping_fee = db.Column(db.Float, nullable=False, default=250.0)
        total_amount = db.Column(db.Float, nullable=False)
        status = db.Column(db.String(100), default="Pending")
        created_at = db.Column(db.DateTime, default=db.func.now())

        payment_method = db.Column(db.String(20), nullable=False, default='COD')
        payment_status = db.Column(db.String(30), nullable=False, default='Pending') 

        items = db.relationship("Order_Item", backref='order', lazy=True, cascade="all, delete-orphan")

class Order_Item(db.Model):
     __tablename__ = "order_items"
     id = db.Column(db.Integer, primary_key=True)
     order_id = db.Column(db.Integer, db.ForeignKey("orders.id"), nullable=False)
     book_id = db.Column(db.Integer, db.ForeignKey("books.id"), nullable=True)
     quantity = db.Column(db.Integer, nullable=False)
     price = db.Column(db.Float, nullable=False)

     book_title = db.Column(db.String(200))
     book_author = db.Column(db.String(200))
    #  book = db.relationship("Books", backref="order_items")
     
