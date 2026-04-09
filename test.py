import time
from datetime import datetime
from time import strftime, strptime

from django.utils.dateparse import parse_datetime


def posted_time_ago(value):
    print(value)

    now = datetime.now()
    print(now - value)

current_time = datetime.now()
# print(current_time)
test_time = '2026-04-05 23:05:00.000000'
formatted_time = parse_datetime(test_time)
# print(formatted_time)
diff = current_time - formatted_time
print(diff.total_seconds())

seconds = diff.total_seconds()
minutes = seconds / 60
hours = minutes / 60
days = hours / 24
weeks = days / 7

if seconds < 60:
    print(f"Seconds ago: {int(seconds)}")
elif minutes < 60:
    print(f"Minutes ago: {int(minutes)}")
elif hours < 24:
    print(f"Hours ago: {int(hours)}")
elif days < 7:
    print(f"Days ago: {int(days)}")
else:
    print(f'Weeks ago: {int(weeks)}')

# posted_time_ago(formatted_time)


