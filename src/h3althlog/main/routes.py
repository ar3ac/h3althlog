from flask import render_template, session, redirect, url_for, flash
from . import bp


@bp.route("/")
def home():
    # Se già loggato → vai in dashboard; altrimenti → login
    if "user" in session:
        return redirect(url_for("main.dashboard"))
    return redirect(url_for("auth.login"))


@bp.route("/dashboard")
def dashboard():
    if "user" not in session:
        flash("Devi fare login per accedere.", "error")
        return redirect(url_for("auth.login"))
    return render_template("dashboard.html", user=session["user"])
