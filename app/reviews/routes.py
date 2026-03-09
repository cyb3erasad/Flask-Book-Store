from flask import render_template, redirect, request, url_for, flash
from flask_login import login_required, current_user
from app.models import Reviews, Books
from app.extension import db
from . import reviews_bp

@reviews_bp.route("/add/<int:book_id>", methods=['POST'])
@login_required
def add_review(book_id):
    book = Books.query.get_or_404(book_id)

    rating = request.form.get('rating')
    review_text = request.form.get('review_text', '').strip()

    if not rating or int(rating) < 1 or int(rating) > 5:
        flash('Please provide a valid rating (1-5 stars)', 'danger')
        return redirect(url_for("books.book_details", book_id=book_id))
    
    new_review = Reviews(
        user_id = current_user.id,
        book_id = book_id,
        rating = int(rating),
        review_text = review_text if review_text else None
    )
    db.session.add(new_review)
    db.session.commit()

    flash('Review submitted successfully!', 'success')
    return redirect(url_for('books.book_details', book_id=book_id))

@reviews_bp.route("/edit/<int:review_id>", methods=['POST'])
@login_required
def edit_review(review_id):
    review = Reviews.query.get_or_404(review_id)

    if review.user_id != current_user.id:
        flash('You can only edit your own reviews', 'danger')
        return redirect(url_for('books.book_details', book_id=review.book_id))
    
    rating = request.form.get('rating')
    review_text = request.form.get('review_text', '').strip()

    if not rating or int(rating) < 1 or int(rating) > 5:
        flash('Please provide a valid rating (1-5 stars)', 'danger')
        return redirect(url_for("books.book_details", book_id=review.book_id))
    
    review.rating = int(rating)
    review.review_text = review_text if review_text else None

    db.session.commit()

    flash('Review updated successfully!', 'success')
    return redirect(url_for('books.book_details', book_id=review.book_id))

@reviews_bp.route("/delete/<int:review_id>")
@login_required
def delete_review(review_id):
    review = Reviews.query.get_or_404(review_id)

    if review.user_id != current_user.id:
        flash('You can only edit your own reviews', 'danger')
        return redirect(url_for('books.book_details', book_id=review.book_id))
    
    book_id = review.book_id
    db.session.delete(review)
    db.session.commit()

    flash('Review deleted successfully!', 'success')
    return redirect(url_for('books.book_details', book_id=book_id))