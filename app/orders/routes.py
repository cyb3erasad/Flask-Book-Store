from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_required, current_user
from app.models import Books, Order, Order_Item
from app.orders import orders_bp
from app.extension import db
from app.admin.decorators import admin_required

@orders_bp.route("/my-orders")
@login_required
def my_orders():
    orders = Order.query.filter_by(user_id=current_user.id).order_by(Order.id.desc()).all()
    return render_template("my_orders.html", orders=orders)

@orders_bp.route("/order/<int:order_id>")
@login_required
def orders_details(order_id):
    order = Order.query.get_or_404(order_id)

    if order.user_id != current_user.id:
        return "Unauthorized", 403
    
    items = Order_Item.query.filter_by(order_id=order.id).all

    return render_template("order_details.html", order=order, items=items)

# Admin order routes

@orders_bp.route("/admin/orders")
@login_required
@admin_required
def admin_all_orders():
    if not current_user.is_admin:
        return "Unauthorized", 403
    
    orders = Order.query.order_by(Order.id.desc()).all()
    return render_template("admin/admin_order.html", orders=orders)

@orders_bp.route("/admin/order/<int:order_id>")
@login_required
@admin_required
def admin_order_details(order_id):
    if not current_user.is_admin:
        return "Unauthorized", 403
    
    order = Order.query.get_or_404(order_id)
    items = Order_Item.query.filter_by(order_id=order.id).all()
    return render_template("admin/admin_order_details.html", order=order, items=items)


@orders_bp.route("/admin/order/<int:order_id>/status/<string:new_status>")
@login_required
@admin_required
def update_order_status(order_id, new_status):
    if not current_user.is_admin:
        return "Unauthorized", 403
    
    order = Order.query.get_or_404(order_id)

    allowed_status = ["Pending", "Processing", "Delivered", "Shipped", "Cancelled"]

    if new_status not in allowed_status:
        flash("Invalid status", "danger")
        return redirect(url_for("orders.admin_all_orders"))
    
    order.status = new_status
    db.session.add(order)
    db.session.commit()

    flash(f"Order {order.id} updated to {new_status}", "success")
    return redirect(url_for("orders.admin_all_orders"))