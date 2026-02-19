from flask import render_template, redirect, flash, url_for, request
from flask_login import login_required
import os
from werkzeug.utils import secure_filename
from app.models import User, Books, Order, Order_Item
from app.extension import db
from .decorators import admin_required
from . import admin_bp

UPLOAD_FOLDER = "app/static/uploads/books"
ALOWED_EXTENSIONS = {"png", "jpg", "jpeg"}

def allowed_filename(filename):
    return "." in filename and filename.rsplit(".",1)[1].lower() in ALOWED_EXTENSIONS

@admin_bp.route("/add-book", methods=["GET", "POST"])
@login_required
@admin_required
def add_book():
    if request.method == "POST":
        title = request.form.get("title")
        author = request.form.get("author")
        price = request.form.get("price")
        stock = request.form.get("stock")
        binding = request.form.get("binding", "Paperback")
        description = request.form.get("description", " ")
        image = request.files.get("image")

        if not title or not author or not price or not stock or not image:
            flash("All fields are required", "danger")
            return redirect(url_for("admin.add_book"))
        image_path = None
        if image and allowed_filename(image.filename):
            filename = secure_filename(image.filename)
            save_path = os.path.join(UPLOAD_FOLDER, filename)
            image.save(save_path)
            image_path = f"uploads/books/{filename}"

        new_book = Books(
            title=title,
            author=author,
            price=float(price),
            stock=int(stock),
            binding=binding,
            description=description,
            image=image_path
        ) 
        db.session.add(new_book)
        db.session.commit()

        flash("Book added successfully", "success")
        return redirect(url_for("admin.manage_books"))
    return render_template("admin/add_book.html")
   

@admin_bp.route("/manage-book")
@login_required
@admin_required
def manage_books():
    books = Books.query.order_by(Books.id.desc()).all()
    return render_template("admin/manage_books.html", books=books)


@admin_bp.route("/delete-book/<int:book_id>")
@login_required
@admin_required
def delete_book(book_id):
    book = Books.query.get_or_404(book_id)

    if book.image:
        image_path = os.path.join("app/static", book.image)
        if os.path.exists(image_path):
            os.remove(image_path)

    db.session.delete(book)
    db.session.commit()
    flash("Book deleted successfully", "success")
    return redirect(url_for("admin.manage_books"))        
