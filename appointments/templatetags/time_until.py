from datetime import datetime

from django import template

register = template.Library()


@register.filter
def time_until(value):
    new_val = value.replace(tzinfo=None)
    diff = new_val - datetime.now()

    seconds = diff.total_seconds()
    minutes = seconds / 60
    hours = minutes / 60
    days = hours / 24
    weeks = days / 7

    if seconds < 60:
        return f"{int(seconds)} seconds"
    elif minutes < 60:
        return f"{int(minutes)} minutes"
    elif hours < 24:
        return f"{int(hours)} hours"
    elif days < 7:
        return f"{int(days)} days"
    else:
        return f"{int(weeks)} weeks"

