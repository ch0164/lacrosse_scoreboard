from django import template
import datetime

register = template.Library()

@register.filter
def duration(td: datetime.timedelta) -> str:
    total_seconds = int(td.total_seconds())
    minutes = total_seconds // 60
    seconds = total_seconds % 60

    return f"{minutes:02}:{seconds:02}"