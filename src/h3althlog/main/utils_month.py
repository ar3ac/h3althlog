# app/main/utils_month.py
from datetime import date, timedelta
import calendar
import locale

# Prova a usare locale italiano (non fatale se assente)
try:
    locale.setlocale(locale.LC_TIME, "it_IT.UTF-8")
except Exception:
    pass

__all__ = ["get_month_range", "get_month_weeks", "month_label"]


def get_month_range(year: int, month: int):
    first = date(year, month, 1)
    _, last_day = calendar.monthrange(year, month)
    last = date(year, month, last_day)
    return first, last


def get_month_weeks(year: int, month: int):
    first, last = get_month_range(year, month)
    # 0 = Lun … 6 = Dom
    start = first - timedelta(days=first.weekday())
    end = last + timedelta(days=(6 - last.weekday()))
    weeks, week, cur = [], [], start
    while cur <= end:
        week.append(cur)
        if len(week) == 7:
            weeks.append(week)
            week = []
        cur += timedelta(days=1)
    if week:
        weeks.append(week)
    return weeks


def month_label(year: int, month: int) -> str:
    d = date(year, month, 1)
    return d.strftime("%B %Y").capitalize()
