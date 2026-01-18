from flask import Blueprint, render_template
from app.models import Books, Order_Item
from app.extension import db

books_bp = Blueprint("books", __name__)

@books_bp.route("/")
def list_books():
    all_books = Books.query.all()

    top_selling = (
        db.session.query(Books, db.func.sum(Order_Item.quantity).label("total_sold"))
        .join(Order_Item, Order_Item.book_id == Books.id)
        .group_by(Books.id)
        .order_by(db.desc("total_sold"))
        .limit(6)
        .all()
    )
    return render_template("home.html", books=all_books, top_selling=top_selling)
