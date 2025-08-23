from datetime import date as dt_date, timedelta, datetime
from datetime import date
from flask import render_template, session, redirect, url_for, flash, request
from . import bp
from .utils import get_week_label, get_diet_label, get_meal_quality_label, get_week_days, get_poop_label, get_single_mood_label, get_week_range
from .services import get_week_entries, week_meals_data, get_meal_quality_counts
from ..models import Entry, db
from .utils_month import get_month_weeks, month_label, get_month_range
import locale

# Imposta italiano (solo se non già fatto altrove)
locale.setlocale(locale.LC_TIME, "it_IT.utf8")

@bp.route("/")
def home():
    # Se già loggato → vai in dashboard; altrimenti → login
    if "user" in session:
        #return redirect(url_for("main.dashboard"))
        return redirect(url_for("main.month_view"))
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

    # recupero counts per i vari pasti
    start, end = get_week_range(monday)  # come fai già


    q_breakfast = get_meal_quality_counts(start, end, "breakfast")
    q_lunch = get_meal_quality_counts(start, end, "lunch")
    q_dinner = get_meal_quality_counts(start, end, "dinner")

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
        q_breakfast=q_breakfast,
        q_lunch=q_lunch,
        q_dinner=q_dinner
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
        return redirect(url_for("entries.new_entry", date=day.isoformat()))

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


@bp.route("/month")
def month_view():
    y = request.args.get("y", type=int)
    m = request.args.get("m", type=int)
    today = date.today()
    if not y or not m:
        y, m = today.year, today.month

    start, end = get_month_range(y, m)
    weeks = get_month_weeks(y, m)
    label = month_label(y, m)

    prev_y, prev_m = (y - 1, 12) if m == 1 else (y, m - 1)
    next_y, next_m = (y + 1, 1) if m == 12 else (y, m + 1)

    # QUERY UNICA (solo colonne utili)
    month_entries = (
        db.session.query(
            Entry.date,
            Entry.breakfast_quality,
            Entry.lunch_quality,
            Entry.dinner_quality,
        )
        .filter(Entry.date.between(start, end))
        .all()
    )

    # { date: (b, l, d) }
    entries_map = {
        row[0]: (row[1], row[2], row[3]) for row in month_entries
    }

    return render_template(
        "month.html",
        label=label,
        weeks=weeks,
        entries=entries_map,   # <<< mappa leggera
        y=y, m=m,
        prev=(prev_y, prev_m),
        next=(next_y, next_m),
        today=today,
    )
