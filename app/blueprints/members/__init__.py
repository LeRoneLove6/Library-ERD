from flask import Blueprint


members_bp = Blueprint("members_bp", __name__, url_prefix="/members")

from . import routes
