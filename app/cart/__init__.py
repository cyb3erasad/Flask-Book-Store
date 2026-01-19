from flask import Blueprint

cart_bp = Blueprint("cart", __name__)
from . import routes