from flask import render_template, request, redirect, url_for, session
from app.models import Books, Order_Item, Reviews
from app.extension import db
from flask_login import current_user
from . import books_bp

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

@books_bp.route("/search")
def search_books():
    query = request.args.get("q", "").strip()

    if not query:
        return redirect(url_for("books.list_books"))
    
    books = Books.query.filter(
        db.or_(
            Books.title.ilike(f"%{query}%"),
            Books.author.ilike(f"%{query}%")
        )
    ).all()

    return render_template("home.html", search_query=query, books=books, top_selling=[])

@books_bp.route("/book/<int:book_id>")
def book_details(book_id):
    book = Books.query.get_or_404(book_id)

    cart = session.get("cart", {})
    cart_amount = sum(cart.values())

    reviews = Reviews.query.filter_by(book_id=book_id).order_by(Reviews.created_at.desc()).all()

    avg_rating = 0
    if reviews:
        avg_rating = sum(r.rating for r in reviews) / len(reviews)

    user_review = None
    if current_user.is_authenticated:
        user_review = Reviews.query.filter_by(book_id=book_id, user_id=current_user.id).first()

    return render_template("book_detail.html",
                            book=book,
                            cart_amount=cart_amount,
                            reviews=reviews,
                            avg_rating=avg_rating,
                            user_review=user_review)
