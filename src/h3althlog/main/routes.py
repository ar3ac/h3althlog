from datetime import date, timedelta, datetime
from flask import render_template, session, redirect, url_for, flash, request
from . import bp
from .utils import get_week_label, get_diet_label, get_meal_quality_label, get_week_days, get_poop_label, get_single_mood_label, get_week_range, get_diet_icon, format_steps_full, format_weight, get_mood_icon, get_poop_icon, safe_average, get_diet_summary_label
from .services import get_week_entries, week_meals_data, get_meal_quality_counts
from ..models import Entry, db
from .utils_month import get_month_weeks, month_label, get_month_range
from collections import Counter
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
        start_date = date.fromisoformat(
            start_str) if start_str else date.today()
    except ValueError:
        start_date = date.today()

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
        current_date=date.today(),
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
    # Aggiungiamo il parametro 'view' per il toggle
    view_mode = request.args.get("view")
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
            Entry.steps,
            Entry.weight,
            Entry.breakfast_diet,
            Entry.lunch_diet,
            Entry.dinner_diet,
            Entry.mood,
            Entry.poop_quality,
        )
        .filter(Entry.date.between(start, end))
        .all()
    )

    entries_map = {
        row[0]: row[1:]
        for row in month_entries
    }

    # Calcolo summary qualità pasti per il mese
    meal_quality_summary = {}
    diet_summary = {}
    steps_summary = {}
    weight_summary = {}
    mood_summary = {}
    poop_summary = {}
    if not view_mode or view_mode == 'default':
        breakfast_q = [row[1] for row in month_entries if row[1] is not None]
        lunch_q = [row[2] for row in month_entries if row[2] is not None]
        dinner_q = [row[3] for row in month_entries if row[3] is not None]

        def get_quality_stats(qualities: list[int]) -> dict:
            """Calcola statistiche di qualità per un tipo di pasto."""
            if not qualities:
                return {"total": 0, "good_p": 0, "normal_p": 0, "bad_p": 0, "good_c": 0, "normal_c": 0, "bad_c": 0}

            counts = Counter(qualities)
            total = len(qualities)

            return {
                "total": total,
                "good_p": counts.get(1, 0) / total * 100,
                "normal_p": counts.get(2, 0) / total * 100,
                "bad_p": counts.get(3, 0) / total * 100,
                "good_c": counts.get(1, 0),
                "normal_c": counts.get(2, 0),
                "bad_c": counts.get(3, 0),
            }

        meal_quality_summary = {
            "breakfast": get_quality_stats(breakfast_q),
            "lunch": get_quality_stats(lunch_q),
            "dinner": get_quality_stats(dinner_q),
        }

    if view_mode == 'diet':
        breakfast_d = [row[6] for row in month_entries if row[6] is not None]
        lunch_d = [row[7] for row in month_entries if row[7] is not None]
        dinner_d = [row[8] for row in month_entries if row[8] is not None]

        def get_diet_stats(diets: list[int]) -> dict:
            """Calcola statistiche di dieta per un tipo di pasto."""
            if not diets:
                return {"total": 0, "stats": []}

            counts = Counter(diets)
            total = len(diets)
            
            stats = []
            # Itera su tutti i tipi di dieta possibili per verificare se esistono nei dati
            for diet_id in range(1, 6): # da 1 a 5
                count = counts.get(diet_id, 0)
                if count > 0:
                    stats.append({
                        "name": get_diet_summary_label(diet_id),
                        "icon": get_diet_icon(diet_id),
                        "count": count,
                        "percentage": count / total * 100
                    })
            
            stats.sort(key=lambda x: x['count'], reverse=True)

            return {"total": total, "stats": stats}

        diet_summary = {
            "breakfast": get_diet_stats(breakfast_d),
            "lunch": get_diet_stats(lunch_d),
            "dinner": get_diet_stats(dinner_d),
        }

    if view_mode == 'steps':
        # Get all steps values, filtering out None and 0
        steps_values = [row[4] for row in month_entries if row[4] is not None and row[4] > 0]
        avg_steps = safe_average(steps_values)
        if avg_steps is not None:
            avg_steps = int(avg_steps)
        steps_summary = {
            "average": avg_steps,
            "count": len(steps_values)
        }

    if view_mode == 'weight':
        # Prepara i dati per il grafico del peso
        weight_data = {day: data[4] for day, data in entries_map.items() if data[4] is not None and data[4] > 0}

        chart_labels = []
        chart_values = []

        # Itera su tutti i giorni del mese per avere un asse X continuo
        current_day = start
        while current_day <= end:
            # Mostra solo i giorni del mese corrente nel grafico
            if current_day.month == m:
                chart_labels.append(current_day.strftime('%d/%m'))
                chart_values.append(weight_data.get(current_day)) # Sarà None se non c'è dato
            current_day += timedelta(days=1)

        weight_summary = {
            "labels": chart_labels,
            "data": chart_values,
            "has_data": any(v is not None for v in chart_values)
        }

    if view_mode == 'mood':
        mood_values = [row[9] for row in month_entries if row[9] is not None]

        def get_mood_stats(moods: list[int]) -> dict:
            """Calcola statistiche di umore per il mese."""
            if not moods:
                return {"total": 0, "stats": []}

            counts = Counter(moods)
            total = len(moods)
            
            stats = []
            # Itera su tutti i tipi di umore possibili (1, 2, 3)
            for mood_id in range(1, 4):
                count = counts.get(mood_id, 0)
                if count > 0:
                    stats.append({
                        "name": get_single_mood_label(mood_id).split(" ", 1)[-1], # "Happy", "Normale", "Bad Day"
                        "icon": get_mood_icon(mood_id),
                        "count": count,
                        "percentage": count / total * 100
                    })
            stats.sort(key=lambda x: x['count'], reverse=True)
            return {"total": total, "stats": stats}

        mood_summary = get_mood_stats(mood_values)

    if view_mode == 'poop':
        poop_values = [row[10] for row in month_entries if row[10] is not None]

        def get_poop_stats(poops: list[int]) -> dict:
            """Calcola statistiche di poop quality per il mese."""
            if not poops:
                return {"total": 0, "stats": []}

            counts = Counter(poops)
            total = len(poops)
            stats = []
            # Itera su tutti i tipi di poop quality (1, 2, 3)
            for poop_id in range(1, 4):
                count = counts.get(poop_id, 0)
                if count > 0:
                    # Estrae solo il testo, rimuovendo l'emoji iniziale e spazi
                    full_label = get_poop_label(poop_id)
                    # Trova il primo spazio e prende il testo che segue
                    name_only = full_label.split(" ", 1)[-1] if " " in full_label else full_label
                    stats.append({
                        "name": name_only,
                        "icon": get_poop_icon(poop_id),
                        "count": count,
                        "percentage": count / total * 100
                    })
            stats.sort(key=lambda x: x['count'], reverse=True)
            return {"total": total, "stats": stats}
        poop_summary = get_poop_stats(poop_values)

    return render_template(
        "month.html",
        label=label,
        weeks=weeks,
        entries=entries_map,   # <<< mappa leggera
        y=y, m=m,
        prev=(prev_y, prev_m),
        next=(next_y, next_m),
        today=today,
        view_mode=view_mode,  # Passiamo la modalità al template
        meal_quality_summary=meal_quality_summary,
        diet_summary=diet_summary,
        steps_summary=steps_summary,
        weight_summary=weight_summary,
        mood_summary=mood_summary,
        poop_summary=poop_summary,
        get_diet_icon=get_diet_icon,
        get_diet_label=get_diet_label,
        format_steps_full=format_steps_full,
        format_weight=format_weight,
        get_mood_icon=get_mood_icon,
        get_poop_icon=get_poop_icon,
    )
