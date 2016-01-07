from sys import argv

from datetime import datetime

ROUNDTO = 5

# print(argv[1])
dt = datetime.strptime(argv[1], "%a %b %d %H:%M:%S %Z %Y")
minute = dt.minute // ROUNDTO * ROUNDTO; # Round down to nearest ROUNDTO minutes
# print(dt)
# print(minute)
dtRounded = datetime(dt.year, dt.month, dt.day, dt.hour, minute)
# print(dtRounded)
filename = dtRounded.strftime('%Y%m%d-%H%M')
print(filename)
