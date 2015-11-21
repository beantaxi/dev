import datetime
import getpass
import os.path
import sys

user = getpass.getuser()
folder = os.path.join("/home", user)
heartbeatFile = os.path.join(folder, "heartbeat")
with open(heartbeatFile, "a") as dst:
	now = datetime.datetime.now()
	idExtract = sys.argv[1]
	s = "{} - {}".format(now, idExtract)
	print(s, file=dst)


