from flask import Blueprint

bp = Blueprint("entries", __name__)

from . import routes  # noqa: F401
