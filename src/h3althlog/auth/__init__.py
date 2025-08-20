from flask import Blueprint

# Blueprint per tutto ciò che riguarda l'autenticazione
# Nessun url_prefix: /login e /logout restano invariati.
bp = Blueprint("auth", __name__)

# Importa le route per registrarle sul blueprint
from . import routes  # noqa: F401
