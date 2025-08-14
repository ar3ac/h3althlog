import os
from flask import render_template, request, redirect, url_for, flash, session
from argon2 import PasswordHasher

from . import bp                    # il Blueprint "auth" creato in auth/__init__.py
from ..extensions import limiter    # rate limiter condiviso

# Leggiamo le credenziali dall'ambiente (in dev le fornisce .env caricato in app.py)
ADMIN_USER = os.getenv("ADMIN_USER", "")
ADMIN_PASS_HASH = os.getenv("ADMIN_PASS_HASH", "")

ph = PasswordHasher()


@bp.route("/login", methods=["GET", "POST"])
@limiter.limit("5 per minute", methods=["POST"])
def login():
    # Se sei già loggato, non ha senso rivedere il form
    if "user" in session:
        # NOTE: per ora la dashboard è ancora senza blueprint
        return redirect(url_for("main.dashboard"))

    if request.method == "GET":
        # blueprint loader: cerca in auth/templates/login.html
        return render_template("login.html")

    # POST: verifica credenziali
    username = request.form.get("username", "").strip()
    password = request.form.get("password", "")

    if username != ADMIN_USER:
        flash("Credenziali non valide", "error")
        return redirect(url_for("auth.login"))

    try:
        ph.verify(ADMIN_PASS_HASH, password)
    except Exception:
        flash("Credenziali non valide", "error")
        return redirect(url_for("auth.login"))

    # Ok: segna la sessione e vai in dashboard
    session["user"] = username
    flash(f"Benvenuto, {username}!", "success")
    return redirect(url_for("main.dashboard"))


@bp.route("/logout")
def logout():
    session.clear()
    flash("Logout effettuato", "success")
    return redirect(url_for("auth.login"))
