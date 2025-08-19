from ..models import Entry
from .utils import get_week_range


from datetime import date

def get_week_entries(start: date | None = None):
    start, end = get_week_range(start)
    return (
        Entry.query
        .filter(Entry.date >= start, Entry.date <= end)
        .order_by(Entry.date.asc())
        .all()
    )
