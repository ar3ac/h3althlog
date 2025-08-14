from .main import bp as main_bp
from flask import flash, redirect, url_for
from functools import wraps
from .auth import bp as auth_bp
from .extensions import csrf, limiter
import os
from datetime import timedelta
from flask import Flask, redirect, url_for, session
from dotenv import load_dotenv

# 1) Carica .env in dev
load_dotenv(override=False)

# 2) Crea l'app
app = Flask(__name__)

# 3) Config segreti e cookie
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "")
app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
    # ➜ metti True in produzione (HTTPS)
    SESSION_COOKIE_SECURE=False,
    PERMANENT_SESSION_LIFETIME=timedelta(hours=12),
    RATELIMIT_HEADERS_ENABLED=True,          # header diagnostici per limiter
)

# Applica durata "permanent"


@app.before_request
def _apply_session_lifetime():
    session.permanent = True


# 4) Inizializza estensioni (importa istanze e collegatele all'app)
csrf.init_app(app)
limiter.init_app(app)

# 5) Registra il blueprint auth
app.register_blueprint(auth_bp)

# 6) (Per ora) home e dashboard restano qui
app.register_blueprint(main_bp)







# def login_required(view_func):
#     @wraps(view_func)
#     def wrapped(*args, **kwargs):
#         if "user" not in session:
#             flash("Devi fare login per accedere.", "error")
#             return redirect(url_for("auth.login"))
#         return view_func(*args, **kwargs)
#     return wrapped
