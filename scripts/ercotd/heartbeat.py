import datetime

with open("/home/ubuntu/work/euclid/scripts/heartbeat", "a") as dst:
	now = datetime.datetime.now()
	s = "{} beat".format(now)
	print(s, file=dst)


