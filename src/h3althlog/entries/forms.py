from flask_wtf import FlaskForm
from wtforms import DateField, IntegerField, FloatField, TextAreaField, SubmitField, SelectField
from wtforms.validators import DataRequired, Optional


class FloatCommaField(FloatField):
    def process_formdata(self, valuelist):
        if valuelist:
            # sostituisci la virgola con punto
            val = valuelist[0].replace(",", ".")
            try:
                self.data = float(val)
            except ValueError:
                self.data = None
                raise ValueError(self.gettext("Inserisci un numero valido"))


class EntryForm(FlaskForm):
    date = DateField("Data", validators=[DataRequired()], format="%Y-%m-%d")

    breakfast_quality = SelectField(
        "Qualità colazione",
        choices=[("0", "--- Seleziona ---"), (1, "🟢 Ottima"),
                 (2, "🟡 Normale"), (3, "🔴 Esagerata")],
        coerce=int,
        validators=[Optional()]
    )
    lunch_quality = SelectField(
        "Qualità pranzo",
        choices=[("0", "--- Seleziona ---"), (1, "🟢 Ottima"),
                 (2, "🟡 Normale"), (3, "🔴 Esagerata")],
        coerce=int,
        validators=[Optional()]
    )
    dinner_quality = SelectField(
        "Qualità cena",
        choices=[("0", "--- Seleziona ---"), (1, "🟢 Ottima"),
                 (2, "🟡 Normale"), (3, "🔴 Esagerata")],
        coerce=int,
        validators=[Optional()]
    )

    breakfast_diet = SelectField(
        "Dieta colazione", 
        choices=[
            ("0", "--- Seleziona ---"), 
            (1, "🌱 Vegano      "),
            (2, "🥦 Vegetariano"),
            (3, "🐟 Pesce      "),
            (4, "🍗 Pollo      "),
            (5, "🥩 Carne rossa"),
        ],
        coerce=int,
        validators=[Optional()]
    )
    lunch_diet = SelectField(
        "Dieta pranzo",
        choices=[
            ("0", "--- Seleziona ---"), (1, "🌱 Vegano      "),
            (2, "🥦 Vegetariano"),
            (3, "🐟 Pesce      "),
            (4, "🍗 Pollo      "),
            (5, "🥩 Carne rossa"),
        ],
        coerce=int,
        validators=[Optional()]
    )
    dinner_diet = SelectField(
        "Dieta cena",
        choices=[
            ("0", "--- Seleziona ---"), (1, "🌱 Vegano      "),
            (2, "🥦 Vegetariano"),
            (3, "🐟 Pesce      "),
            (4, "🍗 Pollo      "),
            (5, "🥩 Carne rossa"),
        ],
        coerce=int,
        validators=[Optional()]
    )

    mood = SelectField(
        "Umore", 
        choices=[
            ("0", "--- Seleziona ---"),
            (1, "😀 Happy"),
            (2, "🙂 Normale"), 
            (3, "😔 Bad Day")
    ],
    coerce=int,
    validators=[Optional()]
    )

    poop_quality = SelectField(
        "Qualità cacca",
        choices=[
            ("0", "--- Seleziona ---"), 
            (1, "😎 Showtime!"),
            (2, "🙂 Normale"),
            (3, "🤢 Pessima")
        ],
        coerce=int,
        validators=[Optional()]
    )
    medications = TextAreaField("Farmaci", validators=[Optional()])
    comment = TextAreaField("Commento", validators=[Optional()])
    steps = IntegerField("Passi", validators=[Optional()])

    weight = FloatCommaField("Peso (kg)", validators=[Optional()])
    pressure_sys = IntegerField("Pressione sistolica (SYS)", validators=[Optional()])
    pressure_dia = IntegerField("Pressione diastolica (DIA)", validators=[Optional()])


    submit = SubmitField("Salva")


