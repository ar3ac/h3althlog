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
