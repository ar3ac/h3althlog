from datetime import date as dt_date, timedelta
from flask import render_template, session, redirect, url_for, flash, request
from . import bp
from .utils import get_week_label, get_meals_with_diet, get_mood_label, get_steps_label, get_week_days
from .services import get_week_entries


@bp.route("/")
def home():
    # Se già loggato → vai in dashboard; altrimenti → login
    if "user" in session:
        return redirect(url_for("main.dashboard"))
    return redirect(url_for("auth.login"))


@bp.route("/dashboard")
def dashboard():
    from datetime import timedelta, date as dt_date
    from flask import request

    # --- calcolo settimana corrente o da query ---
    start_str = request.args.get("start")
    try:
        start_date = dt_date.fromisoformat(
            start_str) if start_str else dt_date.today()
    except ValueError:
        start_date = dt_date.today()

    # Label e giorni della settimana (usa le tue utils)
    week_label = get_week_label(today=start_date)
    week_days = get_week_days(today=start_date)

    # Recupera entries della settimana
    entries_list = get_week_entries(start=start_date)
    entries_map = {e.date: e for e in entries_list}

    # Link navigazione
    prev_start = start_date - timedelta(days=7)
    next_start = start_date + timedelta(days=7)

    # Calcoli già esistenti
    meals = get_meals_with_diet(entries_list)
    mood_label = get_mood_label(entries_list)
    steps_label = get_steps_label(entries_list)

    return render_template(
        "dashboard.html",
        user=session.get("user"),   # o come passi il nome
        week_label=week_label,
        week_days=week_days,
        entries=entries_map,        # <--- dict usato nel template
        prev_start=prev_start,
        next_start=next_start,
        start_date=start_date,
        meals=meals,
        mood_label=mood_label,
        steps_label=steps_label,
    )
