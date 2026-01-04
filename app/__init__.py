from flask import Flask
from .extension import db, login_manager, migrate

def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")

    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    

    from auth import auth_bp
    from books import books_bp
    from cart import cart_bp
    from orders import orders_bp
    from admin import admin_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(books_bp)
    app.register_blueprint(cart_bp)
    app.register_blueprint(orders_bp)
    app.register_blueprint(admin_bp)


    return app
