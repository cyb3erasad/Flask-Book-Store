from flask import render_template, redirect, url_for, request, flash
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user, logout_user, login_required
from . import auth_bp
from app.models import User
from app.extension import db

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        full_name = request.form.get("full_name")
        email = request.form.get("email")
        password = request.form.get("password")

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("Email already exist", "danger")
            return redirect(url_for("auth.register"))
        
        hashed_password = generate_password_hash(password)

        user = User(full_name = full_name,
                    email = email,
                    password = hashed_password)
        
        db.session.add(user)
        db.session.commit()
        flash("Account created successfully! Please login", "success")
        return redirect(url_for("auth.login"))
    return render_template("register.html")

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            flash("Logged in successfully", "success")
            return redirect(url_for("books.list_books"))
        flash("Invalid email or password", "danger")
    return render_template("login.html")
    
@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out successfully", "info")
    return redirect(url_for("auth.login"))