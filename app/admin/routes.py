from flask import render_template
from app.models import Books, Order, Order_Item, User
from flask_login import login_required
from app.extension import db
from . import admin_bp
from .decorators import admin_required


@admin_bp.route("/dashboard")
@login_required
@admin_required
def dashboard():
    total_books = Books.query.count()
    total_users = User.query.count()
    total_oders = Order.query.count()

    total_revenue = db.session.query(
        db.func.sum(Order_Item.price * Order_Item.quantity)
    ).scalar() or 0

    recent_orders = Order.query.order_by(Order.id.desc()).limit(10).all()

    top_selling = (
        db.session.query(
            Books, db.func.sum(Order_Item.quantity).label("total_sold")
        )
        .join(Order_Item, Order_Item.book_id == Books.id)
        .group_by(Books.id)
        .order_by(db.desc("total_sold"))
        .limit(5)
        .all()
    )

    low_stock_books = Books.query.filter(Books.stock <=5).order_by(Books.stock).all()

    return render_template(
        "admin/dashboard.html",
        total_books=total_books,
        total_oders=total_oders,
        total_users=total_users,
        total_revenue=total_revenue,
        recent_orders=recent_orders,
        top_selling=top_selling,
        low_stock_books=low_stock_books
    )