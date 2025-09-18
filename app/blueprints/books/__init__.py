from flask import Blueprint

books_bp = Blueprint('books_bp', __name__, url_prefix='/books')

from . import routes
