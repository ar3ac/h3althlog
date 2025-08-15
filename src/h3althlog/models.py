from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class Entry(db.Model):
    __tablename__ = "entries"

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, unique=True, nullable=False)

    # Qualità pasti (1 = bene, 2 = normale, 3 = male)
    breakfast_quality = db.Column(db.Integer, nullable=True)
    lunch_quality = db.Column(db.Integer, nullable=True)
    dinner_quality = db.Column(db.Integer, nullable=True)

    # Tipo dieta (1 = Vegano, 2 = Vegetariano, 3 = Pesce, 4 = Pollo, 5 = Carne rossa)
    breakfast_diet = db.Column(db.Integer, nullable=True)
    lunch_diet = db.Column(db.Integer, nullable=True)
    dinner_diet = db.Column(db.Integer, nullable=True)

    # Altri dati
    mood = db.Column(db.String(50))         # emoji o testo breve
    poop_quality = db.Column(db.String(50))  # emoji o testo breve
    medications = db.Column(db.Text)
    comment = db.Column(db.Text)
    steps = db.Column(db.Integer)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<Entry {self.date}>"

    @staticmethod
    def diet_labels():
        """Mappatura codice → nome categoria."""
        return {
            1: "Vegano",
            2: "Vegetariano",
            3: "Pesce",
            4: "Pollo",
            5: "Carne rossa"
        }

    @staticmethod
    def diet_colors():
        """Mappatura codice → colore HEX."""
        return {
            1: "#4CAF50",  # Vegano
            2: "#388E3C",  # Vegetariano
            3: "#2E7D32",  # Pesce
            4: "#FF9800",  # Pollo
            5: "#F44336"   # Carne rossa
        }
