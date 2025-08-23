from collections import Counter
from ..models import Entry
from .utils import get_week_range, get_week_days, meal_quality_to_class
from datetime import date


def get_week_entries(start: date | None = None):
    start, end = get_week_range(start)
    return (
        Entry.query
        .filter(Entry.date >= start, Entry.date <= end)
        .order_by(Entry.date.asc())
        .all()
    )


def week_meals_data(today=None):
    """Ritorna i dati settimanali con 3 pallini per ogni pasto."""
    week_days = get_week_days(today)
    data = {}

    for d in week_days:
        entry = Entry.query.filter_by(date=d).first()
        if entry:
            data[d] = {
                "entry": entry,
                "meals": [
                    meal_quality_to_class(entry.breakfast_quality),
                    meal_quality_to_class(entry.lunch_quality),
                    meal_quality_to_class(entry.dinner_quality),
                ]
            }
        else:
            data[d] = {
                "entry": None,
                "meals": ["gray", "gray", "gray"]
            }

    return data


def get_meal_quality_counts(start: date, end: date, meal: str) -> dict:
    """
    Conteggi settimanali della qualità per un pasto ('breakfast'|'lunch'|'dinner').
    Ritorna {labels, data, total} con ordine Bene(1), Normale(2), Male(3).
    """
    if meal not in {"breakfast", "lunch", "dinner"}:
        raise ValueError("meal deve essere 'breakfast'|'lunch'|'dinner'")

    col = getattr(Entry, f"{meal}_quality")
    rows = (Entry.query
            .with_entities(col)
            .filter(Entry.date >= start, Entry.date <= end)
            .all())

    vals = [r[0] for r in rows if r[0] is not None]
    c = Counter(vals)
    data = [c.get(1, 0), c.get(2, 0), c.get(3, 0)]
    return {"labels": ["Bene", "Normale", "Male"], "data": data, "total": sum(data)}
