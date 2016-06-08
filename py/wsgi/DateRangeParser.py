import re

class DateRangeParser:
	@classmethod
	def getDateRange (cls, datestr):
		if cls.isDateTime(datestr):
			dtRange = cls.parseDateTime(datestr)
		elif cls.isSingleDay(datestr):
			dtRange = cls.parseSingleDay(datestr)
		elif cls.isDayRange(datestr):
			dtRange = cls.parseDayRange(datestr)
		else:
			raise Exception("Invalid datestr %s" % datestr)
		return dtRange


	@classmethod
	def isDateTime (cls, datestr):
		rx = "^\d{12}$"
		flag = re.search(rx, datestr)
		return flag


	@classmethod
	def isDayRange (cls, datestr):
		rx = "^\d{8}-\d{8}$"
		flag = re.search(rx, datestr)
		return flag


	@classmethod
	def isSingleDay (cls, datestr):
		rx = "^\d{8}$"
		flag = re.search(rx, datestr)
		return flag 


	@classmethod
	def isValid (cls, datestr):
		flag = cls.isDateTime(datestr) or cls.isSingleDay(datestr) or cls.isDayRange(datestr)
		return flag

	@classmethod
	def parseDateTime (cls, datestr):
		dtRange = (datestr, datestr)
		return dtRange

	@classmethod
	def parseDayRange (cls, datestr):
		rx = "^(\d{8})-(\d{8})$"
		groups = re.search(rx, datestr)
		dtStart = groups.group(1) + '000000'
		dtEnd = groups.group(2) + '235959'
		dtRange = (dtStart, dtEnd)
		return dtRange

	@classmethod
	def parseSingleDay (cls, datestr):
		dtStart = datestr + "000000"
		dtEnd = datestr + "235959"
		dtRange = (dtStart, dtEnd)
		return dtRange
		dtRange = ("No Clue", "No Clue")
