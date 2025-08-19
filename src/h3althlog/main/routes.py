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
    # Capire da che data partire
    # prende il parametro start dall'url e lo converte da str a data
    start_str = request.args.get("start")
    try:
        start_date = dt_date.fromisoformat(
            start_str) if start_str else dt_date.today()
    except ValueError:
        start_date = dt_date.today()

    # Creare la label settimana
    week_label = get_week_label(today=start_date)

    # 3. Date prev/next
    # prima calcolo il lunedì della start_date
    monday = start_date - timedelta(days=start_date.weekday())
    # poi calcolo il lunedì della settimana precedente e successiva
    prev_start = monday - timedelta(days=7)
    next_start = monday + timedelta(days=7)

    # 5. Lista giorni della settimana
    week_days = get_week_days(today=start_date)

    # 6. Recupero entries della settimana
    entries_list = get_week_entries()   # <-- usa la tua funzione services.py
    entries_map = {e.date: e for e in entries_list}


    return render_template(
        "dashboard.html",
        week_label=week_label,
        start_date=start_date,
        prev_start=prev_start,
        next_start=next_start,
        week_days=week_days,
        entries=entries_map,
        current_date=dt_date.today(),
    )
