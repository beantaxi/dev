# import urllib.parse
import sys
import traceback
from . import dateRangeParser
from . import utils

def application (env, start_response):
	start_response('200 OK', [('Content-type', 'text/html')])
	resp = ""
	path = env['PATH_INFO']
	parts = path.split('/')
	extractId = parts[2]
	datestr = parts[3]
	
	try:
		utils.validateRequestMethod(env, ['GET'])
		dtRange = dateRangeParser.getDateRange(datestr)
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
		lines = utils.tracebackAsLines(tb)
		for line in lines:
			resp += line + "\r"
	return [resp.encode('utf-8')]
