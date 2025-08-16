from datetime import date, timedelta


from datetime import date, timedelta
import locale

# Imposta la lingua italiana per i mesi
locale.setlocale(locale.LC_TIME, "it_IT.utf8")

# --- RANGE SETTIMANA ---
def get_week_range(today: date | None = None) -> tuple[date, date]:
    if today is None:
        today = date.today()
    start = today - timedelta(days=today.weekday())  # lun
    end = start + timedelta(days=6)                  # dom
    return start, end


def get_week_label(today: date | None = None) -> str:
    """Ritorna un'etichetta tipo 'Settimana 11-17 Agosto 2025'."""
    if today is None:
        today = date.today()

    start = today - timedelta(days=today.weekday())  # lunedì
    end = start + timedelta(days=6)                  # domenica

    # Se mese di inizio e fine coincidono
    if start.month == end.month:
        label = f"Settimana {start.day}-{end.day} {end.strftime('%B %Y')}"
    else:
        # Caso raro: settimana a cavallo di due mesi
        label = f"Settimana {start.day} {start.strftime('%B')} - {end.day} {end.strftime('%B %Y')}"

    return label


def get_meal_quality_label(avg: float) -> str:
    """Trasforma la media numerica in etichetta + emoji."""
    if avg < 1.5:
        return "Ottima 🟢"
    elif avg < 2.5:
        return "Normale 🟡"
    else:
        return "Scarsa 🔴"


# def get_meals_breakdown(colazione: list[int], pranzo: list[int], cena: list[int]) -> dict:
#     """
#     Calcola la media settimanale per ogni pasto
#     e ritorna un dizionario con le etichette pronte.
#     """
#     def safe_avg(values: list[int]) -> float:
#         return sum(values) / len(values) if values else 0

#     return {
#         "colazione": get_meal_quality_label(safe_avg(colazione)),
#         "pranzo": get_meal_quality_label(safe_avg(pranzo)),
#         "cena": get_meal_quality_label(safe_avg(cena)),
#     }


def get_diet_label(value: int) -> str:
    """Ritorna etichetta + emoji per una dieta singola."""
    mapping = {
        1: "Vegano 🥦",
        2: "Vegetariano 🥦🧀🍳",
        3: "Pesce 🐟",
        4: "Pollo 🍗",
        5: "Carne rossa 🥩"
    }
    return mapping.get(value, "N/A")


def get_diet_prevalence(values: list[int]) -> str:
    """Trova la dieta più frequente in una lista settimanale."""
    if not values:
        return "Nessun dato 🤷"
    from collections import Counter
    most_common, _ = Counter(values).most_common(1)[0]
    return get_diet_label(most_common)


def get_meals_with_diet(colazione_q: list[int], pranzo_q: list[int], cena_q: list[int],
                        colazione_d: list[int], pranzo_d: list[int], cena_d: list[int]) -> dict:
    """Combina qualità e dieta per ogni pasto."""
    def safe_avg(values: list[int]) -> float:
        return sum(values) / len(values) if values else 0

    return {
        "colazione": {
            "quality": get_meal_quality_label(safe_avg(colazione_q)),
            "diet": get_diet_prevalence(colazione_d)
        },
        "pranzo": {
            "quality": get_meal_quality_label(safe_avg(pranzo_q)),
            "diet": get_diet_prevalence(pranzo_d)
        },
        "cena": {
            "quality": get_meal_quality_label(safe_avg(cena_q)),
            "diet": get_diet_prevalence(cena_d)
        }
    }


# --- UMORE ---
MOOD_MAP = {"😊": 1, "😐": 2, "😞": 3}
def get_mood_label(moods: list[str]) -> str:
    if not moods:
        return "Nessun dato 🤷"
    nums = [MOOD_MAP.get(m, 2) for m in moods]  # default neutro se manca
    avg = sum(nums) / len(nums)
    if avg < 1.5:
        return "Positivo 😊"
    elif avg < 2.5:
        return "Neutro 😐"
    else:
        return "Negativo 😞"


# --- PASSI ---
def get_steps_label(steps: list[int]) -> str:
    if not steps:
        return "Nessun dato 🤷"
    avg = int(sum(steps) / len(steps))
    formatted = f"{avg:,}".replace(",", ".")
    if avg >= 10000:
        return f"🚶 {formatted} 🟢"
    else:
        return f"🚶 {formatted} 🔴"


def get_week_days(today: date | None = None) -> list[date]:
    start, end = get_week_range(today)
    return [start + timedelta(days=i) for i in range(7)]
