from flask import Blueprint

reviews_bp = Blueprint("reviews", __name__, url_prefix="/reviews")

from . import routes