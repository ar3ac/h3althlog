from flask_wtf import FlaskForm
from wtforms import DateField, IntegerField, StringField, TextAreaField, SubmitField, SelectField
from wtforms.validators import DataRequired, Optional


class EntryForm(FlaskForm):
    date = DateField("Data", validators=[DataRequired()], format="%Y-%m-%d")

    breakfast_quality = SelectField(
        "Qualità colazione",
        choices=[("0", "--- Seleziona ---"), (1, "Bene ✅"),
                 (2, "Normale 😐"), (3, "Male ❌")],
        coerce=int,
        validators=[Optional()]
    )
    lunch_quality = SelectField(
        "Qualità pranzo",
        choices=[("0", "--- Seleziona ---"), (1, "Bene ✅"),
                 (2, "Normale 😐"), (3, "Male ❌")],
        coerce=int,
        validators=[Optional()]
    )
    dinner_quality = SelectField(
        "Qualità cena",
        choices=[("0", "--- Seleziona ---"), (1, "Bene ✅"),
                 (2, "Normale 😐"), (3, "Male ❌")],
        coerce=int,
        validators=[Optional()]
    )

    breakfast_diet = SelectField(
        "Dieta colazione", 
        choices=[
            ("0", "--- Seleziona ---"), (1, "Vegano      🌱 "),
            (2, "Vegetariano 🥦"),
            (3, "Pesce       🐟"),
            (4, "Pollo       🍗"),
            (5, "Carne rossa 🥩"),
        ],
        coerce=int,
        validators=[Optional()]
    )
    lunch_diet = SelectField(
        "Dieta pranzo",
        choices=[
            ("0", "--- Seleziona ---"), (1, "Vegano      🌱 "),
            (2, "Vegetariano 🥦"),
            (3, "Pesce       🐟"),
            (4, "Pollo       🍗"),
            (5, "Carne rossa 🥩"),
        ],
        coerce=int,
        validators=[Optional()]
    )
    dinner_diet = SelectField(
        "Dieta cena",
        choices=[
            ("0", "--- Seleziona ---"), (1, "Vegano      🌱 "),
            (2, "Vegetariano 🥦"),
            (3, "Pesce       🐟"),
            (4, "Pollo       🍗"),
            (5, "Carne rossa 🥩"),
        ],
        coerce=int,
        validators=[Optional()]
    )

    mood = SelectField(
        "Umore", 
        choices=[
        ("0", "--- Seleziona ---"), (1, "Felice 😊"),
        (2, "Neutro 😐"), (3, "Triste 😢")
    ],
    coerce=int,
    validators=[Optional()]
    )

    poop_quality = SelectField(
        "Qualità cacca",
        choices=[
            ("0", "--- Seleziona ---"), (1, "Bene 😊"),
            (2, "Normale 😐"), (3, "Male 😢")
        ],
        coerce=int,
        validators=[Optional()]
    )
    medications = TextAreaField("Farmaci", validators=[Optional()])
    comment = TextAreaField("Commento", validators=[Optional()])
    steps = IntegerField("Passi", validators=[Optional()])

    submit = SubmitField("Salva")
