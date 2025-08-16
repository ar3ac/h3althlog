from flask import Blueprint, render_template, redirect, url_for, flash, request
from datetime import date as dt_date
from ..models import db, Entry
from .forms import EntryForm
from . import bp
from wtforms import SelectField

def normalize_form_selects(form):
    """
    Scansiona tutti i campi di tipo SelectField in un form
    e converte 0 in None.
    """
    for field in form:
        if isinstance(field, SelectField):
            if field.data == 0:
                field.data = None

@bp.route("/new", methods=["GET", "POST"])
def new_entry():
    form = EntryForm()
    # Se arriva ?date=YYYY-MM-DD, usala
    date_str = request.args.get("date")
    if date_str:
        form.date.data = dt_date.fromisoformat(date_str)
    else:
        form.date.data = dt_date.today()

    if form.validate_on_submit():
        entry = Entry.query.filter_by(date=form.date.data).first()
        if entry:
            flash("Giornata già esistente, usa la modifica.", "warning")
            return redirect(url_for("entries.edit_entry", entry_date=form.date.data))

        normalize_form_selects(form)
        entry = Entry(
            date=form.date.data,
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
            steps=form.steps.data
        )
        db.session.add(entry)
        db.session.commit()
        flash("Giornata aggiunta!", "success")
        return redirect(url_for("main.dashboard"))

    return render_template("form.html", form=form, mode="new")


@bp.route("/<entry_date>/edit", methods=["GET", "POST"])
def edit_entry(entry_date):
    entry = Entry.query.filter_by(date=entry_date).first_or_404()
    form = EntryForm(obj=entry)

    if form.validate_on_submit():
        normalize_form_selects(form)
        form.populate_obj(entry)
        db.session.commit()
        flash("Giornata aggiornata!", "success")
        return redirect(url_for("main.dashboard"))

    return render_template("form.html", form=form, mode="edit")
