import datetime
import sys

with open("/home/ubuntu/work/euclid/scripts/heartbeat", "a") as dst:
	now = datetime.datetime.now()
	idReport = sys.argv[1]
	s = "{} - {}".format(now, idReport)
	print(s, file=dst)


