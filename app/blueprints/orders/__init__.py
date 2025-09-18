from flask import Blueprint


orders_bp = Blueprint("orders_bp", __name__, url_prefix="/orders")

from . import routes
