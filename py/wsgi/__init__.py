# import urllib.parse
import re
import sys
import traceback



def application (env, start_response):
	start_response('200 OK', [('Content-type', 'text/html')])
	resp = ""
	path = env['PATH_INFO']
	parts = path.split('/')
	extractId = parts[2]
	datestr = parts[3]
	
	try:
		dtRange = getDateRange(datestr)
		(dtStart, dtEnd) = dtRange
		resp += "<table>"
		resp += "<tr> <td>extractId</td> <td>{}</td> </tr>".format(extractId)
		resp += "<tr> <td>datestr</td> <td>{}</td> </tr>".format(datestr)
		resp += "<tr> <td>dtStart</td> <td>{}</td> </tr>".format(dtStart)
		resp += "<tr> <td>dtEnd</td> <td>{}</td> </tr>".format(dtEnd)
		resp += "</table>"
	except Exception as ex:
		headers = [('Content-type', 'text/plain')]
		start_response('500 Oops', headers, sys.exc_info())
		resp = ""
		resp += str(ex) + '\r'
		resp += "\r"
		(exType, exInst, tb) = sys.exc_info()
		lines = tracebackAsLines(tb)
		for line in lines:
			resp += line + "\r"
	return [resp.encode('utf-8')]
#	return [resp]


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

def tracebackAsLines (tb):
	lines = []
	for tbLine in traceback.extract_tb(tb):
		(file, ln, fn, msg) = tbLine
		s = "at {}:{} in {}() {}".format(file, ln, fn, msg)
		lines.append(s)
	return lines
