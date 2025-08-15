from flask_wtf import FlaskForm
from wtforms import DateField, IntegerField, StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Optional


class EntryForm(FlaskForm):
    date = DateField("Data", validators=[DataRequired()], format="%Y-%m-%d")

    breakfast_quality = IntegerField("Qualità colazione (1-3)", validators=[Optional()])
    lunch_quality = IntegerField("Qualità pranzo (1-3)", validators=[Optional()])
    dinner_quality = IntegerField("Qualità cena (1-3)", validators=[Optional()])

    breakfast_diet = IntegerField("Dieta colazione (1-5)", validators=[Optional()])
    lunch_diet = IntegerField("Dieta pranzo (1-5)", validators=[Optional()])
    dinner_diet = IntegerField("Dieta cena (1-5)", validators=[Optional()])

    mood = StringField("Umore", validators=[Optional()])
    poop_quality = StringField("Qualità cacca", validators=[Optional()])
    medications = TextAreaField("Farmaci", validators=[Optional()])
    comment = TextAreaField("Commento", validators=[Optional()])
    steps = IntegerField("Passi", validators=[Optional()])

    submit = SubmitField("Salva")
