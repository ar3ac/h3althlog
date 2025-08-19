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
    # Navigazione settimana via query ?start=YYYY-MM-DD (default: oggi)
    start_str = request.args.get("start")
    try:
        start_date = dt_date.fromisoformat(start_str) if start_str else dt_date.today()
    except ValueError:
        start_date = dt_date.today()

    week_label = get_week_label(today=start_date)
    entries = get_week_entries(start=start_date)

    # Indiciamo le date già presenti nel DB
    existing_dates = {e.date for e in entries}

    # Giorni della settimana corrente
    week_days = get_week_days(today=start_date)

    # Prepariamo dati per i link
    day_links = []
    for d in week_days:
        exists = d in existing_dates
        if exists:
            url = url_for("entries.edit_entry", entry_date=d.isoformat())
        else:
            url = url_for("entries.new_entry") + f"?date={d.isoformat()}"

        day_links.append({
            "date": d,
            "exists": exists,
            "url": url
        })

    # Liste di aggregazione
    colazione_q, pranzo_q, cena_q = [], [], []
    colazione_d, pranzo_d, cena_d = [], [], []
    moods, steps = [], []

    for e in entries:
        if e.breakfast_quality:
            colazione_q.append(e.breakfast_quality)
        if e.lunch_quality:
            pranzo_q.append(e.lunch_quality)
        if e.dinner_quality:
            cena_q.append(e.dinner_quality)

        if e.breakfast_diet:
            colazione_d.append(e.breakfast_diet)
        if e.lunch_diet:
            pranzo_d.append(e.lunch_diet)
        if e.dinner_diet:
            cena_d.append(e.dinner_diet)

        if e.mood:
            moods.append(e.mood)
        if e.steps:
            steps.append(e.steps)

    # Preparazione cards
    meals = get_meals_with_diet(colazione_q, pranzo_q, cena_q,
                                colazione_d, pranzo_d, cena_d)
    mood_label = get_mood_label(moods)
    steps_label = get_steps_label(steps)

    # Calcolo link navigazione
    prev_start = start_date - timedelta(days=7)
    next_start = start_date + timedelta(days=7)

    return render_template(
        "dashboard.html",
        prev_start=prev_start,
        next_start=next_start,
        start_date=start_date,
        week_label=week_label,
        meals=meals,
        mood_label=mood_label,
        steps_label=steps_label,
        day_links=day_links
    )
