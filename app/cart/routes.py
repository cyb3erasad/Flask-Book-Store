from flask import render_template, redirect, request, session, flash, url_for
from flask_login import login_required,current_user
from app.cart import cart_bp
from app.extension import db
from app.models import Books, Order, Order_Item
from datetime import datetime

@cart_bp.route("/add-to-cart/<int:book_id>")
def add_to_cart(book_id):
    book = Books.query.get_or_404(book_id)

    cart = session.get("cart", {})
    if str(book_id) in cart:
        cart[str(book_id)] +=1
    else:
        cart[str(book_id)] = 1

    session["cart"] = cart
    flash("Book added to cart", "success")
    return redirect(url_for("books.list_books"))        

@cart_bp.route("/cart")
def view_cart():
    cart = session.get("cart", {})

    books = Books.query.filter(Books.id.in_(cart.keys())).all()

    cart_items = []
    total = 0

    for book in books:
        quantity = cart[str(book.id)]
        subtotal = book.price * quantity
        total += subtotal

        cart_items.append({
            "book": book,
            "quantity": quantity,
            "subtotal": subtotal 
        })    

    return render_template("cart.html", total=total, cart_items=cart_items) 
   
@cart_bp.route("/remove-from-cart/<int:book_id>")
def remove_from_cart(book_id):
    cart = session.get("cart", {})

    cart.pop(str(book_id), None)
    session["cart"] = cart
    flash("book remove from cart", "danger")

    return redirect(url_for("cart.view_cart"))
   

@cart_bp.route("/checkout")
@login_required
def checkout():
    cart = session.get("cart", {})

    if not cart:
        flash("Your cart is empty", "warning")
        return redirect(url_for("cart.view_cart"))
    
    books = Books.query.filter(Books.id.in_(cart.keys())).all()

    total_amount = 0
    for book in books:
        total_amount += book.price * cart[str(book.id)]

    order = Order(
        user_id=current_user.id,
        total_amount=total_amount,
        payment_method="COD",
        status=datetime.utcnow()
    )

    db.session.add(order)
    db.session.commit()

    try:
        for book in books:
            quantity = cart[str(book.id)]

            if book.stock < quantity:
                flash(f"Not enough stock for {book.title}", "danger")
                return redirect(url_for("cart.view_cart"))
            book.stock -= quantity

            order_item = Order_Item(
                order_id=order.id,
                book_id=book.id,
                quantity=quantity,
                price=book.price
            )
            db.session.add(order_item)
        db.session.commit()
        session.pop("cart", None)

        flash("Order placed successfully  (Cash on Delivery)", "success")
        return redirect(url_for("books.list_books"))

    except Exception as a:
        db.session.rollback()
        flash("Error while placing your order", "danger")
        return redirect(url_for("cart.view_cart"))
            




     