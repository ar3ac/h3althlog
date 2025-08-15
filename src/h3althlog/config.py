import os
from datetime import timedelta


class BaseConfig:
    # ——— Segreti ———
    # In dev può essere vuota (Flask ne genera una random ad ogni avvio),
    # in prod deve essere valorizzata da env.
    SECRET_KEY = os.environ.get("SECRET_KEY", "")

    # ——— Session cookie ———
    SESSION_COOKIE_NAME = "h3althlog_session"
    SESSION_COOKIE_HTTPONLY = True       # il cookie non è accessibile da JS
    SESSION_COOKIE_SAMESITE = "Lax"      # difesa CSRF "di base"
    # ⇐ in Prod diventa True (solo su HTTPS)
    SESSION_COOKIE_SECURE = False
    PERMANENT_SESSION_LIFETIME = timedelta(hours=12)  # durata sessione

    # ——— CSRF / Limiter ———
    RATELIMIT_HEADERS_ENABLED = True     # header diagnostici tipo X-RateLimit-*
    # (Se un giorno userai Redis per il limiter, potremo leggere una URI da env qui)

    # ——— Flask ———
    DEBUG = False
    TESTING = False
    TEMPLATES_AUTO_RELOAD = False        # in dev lo accendiamo


    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(BASE_DIR, 'instance', 'h3althlog.db')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    WTF_CSRF_SSL_STRICT = False

class DevConfig(BaseConfig):
    DEBUG = True
    TEMPLATES_AUTO_RELOAD = True
    SESSION_COOKIE_SECURE = False        # in dev usi http://127.0.0.1


class ProdConfig(BaseConfig):
    DEBUG = False
    SESSION_COOKIE_SECURE = True         # cookie solo via HTTPS
    # Piccola guardia: in produzione SECRET_KEY deve essere presente
    if not os.environ.get("SECRET_KEY"):
        raise RuntimeError("SECRET_KEY mancante in produzione.")
