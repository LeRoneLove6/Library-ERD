from flask import Blueprint


items_bp = Blueprint("items_bp", __name__, url_prefix="/items")

from . import routes
