import sys

try:
	n = 1/0
except Exception as ex:
	(exType, exInst, tb) = sys.exc_info()
	for line in tb:
#		print(type(line))
#		(exType, exInst, tb) = line
		print(str(line))
