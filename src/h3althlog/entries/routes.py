from flask import Blueprint, render_template, redirect, url_for, flash, request
from datetime import date as dt_date
from wtforms import SelectField
from ..models import db, Entry
from .forms import EntryForm
from . import bp


def normalize_form_selects(form):
    """
    Converte selezioni 'vuote' in None e normalizza numeri.
    Utile per SelectField che possono restituire '0' (stringa).
    """
    for field in form:
        if isinstance(field, SelectField):
            if field.data in (0, "0", "", None):
                field.data = None
            else:
                # prova a convertirlo a int se è numerico
                try:
                    field.data = int(field.data)
                except (ValueError, TypeError):
                    pass


@bp.route("/new", methods=["GET", "POST"])
def new_entry():
    form = EntryForm()

    # Data di riferimento (da querystring o oggi)
    date_str = request.args.get("date")
    day = dt_date.fromisoformat(date_str) if date_str else dt_date.today()
    form.date.data = day  # hidden nel form

    if form.validate_on_submit():
        # evita duplicati sulla stessa data
        existing = Entry.query.filter_by(date=day).first()
        if existing:
            flash("Giornata già esistente, apro la modifica.", "warning")
            return redirect(url_for("entries.edit_entry", entry_date=day.isoformat()))

        normalize_form_selects(form)

        entry = Entry(
            date=day,
            breakfast_quality=form.breakfast_quality.data,
            lunch_quality=form.lunch_quality.data,
            dinner_quality=form.dinner_quality.data,
            breakfast_diet=form.breakfast_diet.data,
            lunch_diet=form.lunch_diet.data,
            dinner_diet=form.dinner_diet.data,
            mood=form.mood.data,
            poop_quality=form.poop_quality.data,
            medications=form.medications.data,
            comment=form.comment.data,
            steps=form.steps.data,
            weight=form.weight.data,
            pressure_sys=form.pressure_sys.data,
            pressure_dia=form.pressure_dia.data,
        )
        db.session.add(entry)
        db.session.commit()
        flash("Giornata aggiunta!", "success")
        return redirect(url_for("main.day_view", day=day.isoformat()))

    display_day = day.strftime("%A %d %B %Y").capitalize()
    return render_template("form.html", form=form, mode="new",
                           day=day, display_day=display_day)


@bp.route("/<entry_date>/edit", methods=["GET", "POST"])
def edit_entry(entry_date):
    # entry_date arriva come ISO string → convertila a date
    day = dt_date.fromisoformat(entry_date)
    entry = Entry.query.filter_by(date=day).first_or_404()

    form = EntryForm(obj=entry)
    form.date.data = day  # hidden nel form (non modificabile)

    if form.validate_on_submit():
        normalize_form_selects(form)

        # aggiorna campi (non toccare entry.date)
        entry.breakfast_quality = form.breakfast_quality.data
        entry.lunch_quality = form.lunch_quality.data
        entry.dinner_quality = form.dinner_quality.data
        entry.breakfast_diet = form.breakfast_diet.data
        entry.lunch_diet = form.lunch_diet.data
        entry.dinner_diet = form.dinner_diet.data
        entry.mood = form.mood.data
        entry.poop_quality = form.poop_quality.data
        entry.medications = form.medications.data
        entry.comment = form.comment.data
        entry.steps = form.steps.data
        entry.weight = form.weight.data
        entry.pressure_sys = form.pressure_sys.data
        entry.pressure_dia = form.pressure_dia.data

        db.session.commit()
        flash("Giornata aggiornata!", "success")
        return redirect(url_for("main.day_view", day=day.isoformat()))

    display_day = day.strftime("%A %d %B %Y").capitalize()
    return render_template("form.html", form=form, mode="edit",
                           day=day, display_day=display_day)
