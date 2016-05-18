from DateRangeParser import DateRangeParser
from splunge.Exceptions import GeneralClientEx
	
validateMethod('GET')	

path = http.path
if len(path.parts) < 3 or not DateRangeParser.isValid(path[2]):
	msg = "URL path must be of form /extract/[extractId]/YYMMDD or /extract/[extractId]/YYMMDD-YYMMDD"
	raise GeneralClientEx(msg)
extractId = path[1]
datestr = path[2]
dtRange = DateRangeParser.getDateRange(datestr)
(dtStart, dtEnd) = dtRange

# setContentType('text/plain')
# _ = """
# extractId = {{ extractId }}
# dtStart = {{ dtStart }}
# dtEnd = {{ dtEnd }}
# """

