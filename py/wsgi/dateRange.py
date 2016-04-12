def getDateRange (datestr):
	if isDateTime(datestr):
		dtRange = parseDateTime(datestr)
	elif isSingleDay(datestr):
		dtRange = parseSingleDay(datestr)
	elif isDayRange(datestr):
		dtRange = parseDayRange(datestr)
	else:
		raise Exception("Invalid datestr %s" % datestr)
	return dtRange


def isDateTime (datestr):
	rx = "^\d{12}$"
	flag = re.search(rx, datestr)
	return flag


def isDayRange (datestr):
	rx = "^\d{8}-\d{8}$"
	flag = re.search(rx, datestr)
	return flag


def isSingleDay (datestr):
	rx = "^\d{8}$"
	flag = re.search(rx, datestr)
	return flag 


def parseDateTime (datestr):
	dtRange = (datestr, datestr)
	return dtRange


def parseDayRange (datestr):
	rx = "^(\d{8})-(\d{8})$"
	groups = re.search(rx, datestr)
	dtStart = groups.group(1) + '000000'
	dtEnd = groups.group(2) + '235959'
	dtRange = (dtStart, dtEnd)
	return dtRange


def parseSingleDay (datestr):
	dtStart = datestr + "000000"
	dtEnd = datestr + "235959"
	dtRange = (dtStart, dtEnd)
	return dtRange
	dtRange = ("No Clue", "No Clue")

