from datetime import datetime, time, timedelta

today = datetime.today()
start = datetime.combine(today, time(9, 0))
end = datetime.combine(today, time(17, 0))

duration = end - start

slots = []

current = start - timedelta(hours=1)
end = end - timedelta(hours=1)

while current <= end:
    slots.append(current.time())
    current += timedelta(hours=1)

print(slots)


