from ..models import Entry
from .utils import get_week_range


def get_week_entries():
    start, end = get_week_range()
    return (
        Entry.query
        .filter(Entry.date >= start, Entry.date <= end)
        .order_by(Entry.date.asc())
        .all()
    )
