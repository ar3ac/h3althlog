from flask import Blueprint

bp = Blueprint("entries", __name__, template_folder="templates")

from . import routes  # noqa: F401
