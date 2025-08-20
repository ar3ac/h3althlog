from datetime import date as dt_date, timedelta, datetime
from flask import render_template, session, redirect, url_for, flash, request
from . import bp
from .utils import get_week_label, get_diet_label, get_meal_quality_label, get_week_days, get_poop_label, get_single_mood_label
from .services import get_week_entries, week_meals_data
from ..models import Entry, db
import locale

# Imposta italiano (solo se non già fatto altrove)
locale.setlocale(locale.LC_TIME, "it_IT.utf8")

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

    # Recupero dati settimana per il pranzo restituendo un dot colorato
    week_data = week_meals_data()

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
        week_data=week_data,
    )


@bp.route("/day/<day>")
def day_view(day):
    day = datetime.strptime(day, "%Y-%m-%d").date()
    entry = Entry.query.filter_by(date=day).first()

    # etichetta leggibile tipo "Lunedì 18-08-2025"
    day_label = day.strftime("%A %d-%m-%Y").capitalize()

    steps_label = None
    if entry:
        from .utils import get_entry_steps
        steps_label = get_entry_steps(entry.steps)
    else:
        return redirect(url_for("main.new_entry", date_str=day.isoformat()))
    
    return render_template(
        "day.html",
        entry=entry,
        day=day,
        day_label=day_label,
        get_diet_label=get_diet_label,
        get_meal_quality_label=get_meal_quality_label,
        steps_label=steps_label,
        get_poop_label=get_poop_label,
        get_single_mood_label=get_single_mood_label
       )
