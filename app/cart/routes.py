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
   

SHIPPING_FEE = 250.0

@cart_bp.route("/checkout", methods=["GET"])
@login_required
def checkout():
    """Display checkout page with billing form and order summary"""
    cart = session.get("cart", {})

    if not cart:
        flash("Your cart is empty", "warning")
        return redirect(url_for("cart.view_cart"))
    
    # Get all books in cart
    book_ids = [int(book_id) for book_id in cart.keys()]
    books = Books.query.filter(Books.id.in_(book_ids)).all()
    
    # Build order items for display
    order_items = []
    subtotal = 0
    
    for book in books:
        quantity = cart[str(book.id)]
        item_total = book.price * quantity
        subtotal += item_total
        
        order_items.append({
            'book': book,
            'quantity': quantity,
            'item_total': item_total
        })
    
    total = subtotal + SHIPPING_FEE
    
    return render_template(
        "checkout.html",
        order_items=order_items,
        subtotal=subtotal,
        shipping_fee=SHIPPING_FEE,
        total=total,
        user=current_user  # Pre-fill email if needed
    )


@cart_bp.route("/place-order", methods=["POST"])
@login_required
def place_order():
    """Process the order after user submits billing details"""
    cart = session.get("cart", {})
    
    if not cart:
        flash("Your cart is empty", "warning")
        return redirect(url_for("cart.view_cart"))
    
    # Validate all required fields
    required_fields = {
        "first_name": "First name",
        "last_name": "Last name",
        "country": "Country/Region",
        "street_address": "Street address",
        "city": "Town/City",
        "state": "State/County",
        "phone": "Phone number",
        "email": "Email address"
    }
    
    for field, label in required_fields.items():
        if not request.form.get(field) or request.form.get(field).strip() == "":
            flash(f"{label} is required", "danger")
            return redirect(url_for("cart.checkout"))
    
    # Get all books in cart
    book_ids = [int(book_id) for book_id in cart.keys()]
    books = Books.query.filter(Books.id.in_(book_ids)).all()
    
    # Create a dict for quick book lookup
    books_dict = {book.id: book for book in books}
    
    try:
        # Calculate totals
        subtotal = 0
        
        # First, validate stock for all items
        for book_id_str, quantity in cart.items():
            book_id = int(book_id_str)
            book = books_dict.get(book_id)
            
            if not book:
                raise Exception(f"Book with ID {book_id} not found")
            
            if book.stock < quantity:
                raise Exception(f"Not enough stock for '{book.title}'. Available: {book.stock}, Requested: {quantity}")
            
            subtotal += book.price * quantity
        
        shipping_fee = SHIPPING_FEE
        total = subtotal + shipping_fee
        
        # Create the order
        order = Order(
            user_id=current_user.id,
            first_name=request.form["first_name"].strip(),
            last_name=request.form["last_name"].strip(),
            country=request.form["country"].strip(),
            street_address=request.form["street_address"].strip(),
            appartment=request.form.get("appartment", "").strip(),  # Optional
            city=request.form["city"].strip(),
            state=request.form["state"].strip(),
            phone=request.form["phone"].strip(),
            email=request.form["email"].strip(),
            sub_total=subtotal,
            shipping_fee=shipping_fee,
            total_amount=total,
            status="Pending",
            payment_method="COD",
            payment_status="Pending"
        )
        
        db.session.add(order)
        db.session.flush()  # Get order.id without committing
        
        # Create order items and update stock
        for book_id_str, quantity in cart.items():
            book_id = int(book_id_str)
            book = books_dict[book_id]
            
            # Reduce stock
            book.stock -= quantity
            
            # Create order item
            order_item = Order_Item(
                order_id=order.id,
                book_id=book.id,
                quantity=quantity,
                price=book.price
            )
            db.session.add(order_item)
        
        # Commit all changes
        db.session.commit()
        
        # Clear the cart
        session.pop("cart", None)
        
        flash(f"Order #{order.id} placed successfully! Total: Rs {total:.2f} (Cash on Delivery)", "success")
        return redirect(url_for("orders.my_orders"))
    
    except Exception as e:
        db.session.rollback()
        flash(f"Error placing order: {str(e)}", "danger")
        return redirect(url_for("cart.checkout"))






     