from .entries import bp as entries_bp
from .main import bp as main_bp
from flask import flash, redirect, url_for
from functools import wraps
from .auth import bp as auth_bp
from .extensions import csrf, limiter
import os
from datetime import timedelta
from flask import Flask, redirect, url_for, session
from dotenv import load_dotenv
from .config import DevConfig, ProdConfig
from .models import db

# Carica .env in dev
load_dotenv(override=False)

# Crea l'app
app = Flask(__name__)

env = os.getenv("H3ALTHLOG_ENV", "dev").lower()
app.config.from_object(ProdConfig if env in {
                       "prod", "production"} else DevConfig)

db.init_app(app)

with app.app_context():
    db.create_all()

# Applica durata "permanent"
@app.before_request
def _apply_session_lifetime():
    session.permanent = True


csrf.init_app(app)
limiter.init_app(app)


app.register_blueprint(auth_bp)

app.register_blueprint(main_bp)

app.register_blueprint(entries_bp)
