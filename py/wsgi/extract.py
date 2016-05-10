from wsgi import *
from wsgi.DateRangeParser import DateRangeParser
from wsgi.Exceptions import GeneralClientEx
from wsgi.Exceptions import InvalidMethodEx
	
# def www ():
method = app.env['REQUEST_METHOD']
validateMethod(method, ['GET'])	
path = app.env['PATH_INFO']
parts = path.split('/')
if len(parts) < 4 or len(parts[0]) > 0 or not DateRangeParser.isValid(parts[3]):
	msg = "URL path must be of form /extract/[extractId]/YYMMDD or /extract/[extractId]/YYMMDD-YYMMDD"
	raise GeneralClientEx(msg)

path = app.env['PATH_INFO']
parts = path.split('/')
extractId = parts[2]
datestr = parts[3]
dtRange = DateRangeParser.getDateRange(datestr)
(dtStart, dtEnd) = dtRange

args['extractId'] = extractId
args['dtStart'] = dtStart
args['dtEnd'] = dtEnd
