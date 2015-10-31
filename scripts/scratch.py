import datetime
import lxml.html
import math
import random
import time
import urllib.request
import _utils
from IntervalCalculator import IntervalCalculator
from IntervalCalculator import IntervalEnum
from ReportListing import ReportListing
from TimeDelta2 import TimeDelta2


def testDelta (delta):
	sDelta = getDeltaString(delta)
	print("{:32}{:32}".format(str(delta), sDelta))

def testDateTimeStrip ():
e	url = "http://mis.ercot.com/misapp/GetReports.do?reportTypeId=12331&reportTitle=DAM%20Settlement%20Point%20Prices&showHTMLView=&mimicKey"
def adjust (dt, weeks=0, days=0, hours=0, minutes=0, seconds=0, milliseconds=0, microseconds=0):
	localVars = dict(locals())
	del localVars['dt']
	td = datetime.timedelta(**localVars)
	dtNew = dt + td
	return dtNew
	
	with urllib.request.urlopen(url) as src:
		html = lxml.html.parse(src)
	listing = ReportListing(html)
	datetimes = listing.getDateTimes()
	(min, max, avg) = _utils.timeMinMaxAvg(datetimes)
	print("{:24}{:24}{:24}".format(str(min), str(max), str(avg)))

def test1 ():
	dts = [None]*8 
	dtNow = datetime.datetime.now()
	dts[0] = dtNow
	dts[1] = adjust(dtNow, days=1)
	dts[2] = adjust(dtNow, hours=2)
	dts[3] = adjust(dtNow, minutes=3)
	dts[4] = adjust(dtNow, seconds=4)
	dts[5] = adjust(dtNow, days=1, seconds=4)
	dts[6] = adjust(dtNow, hours=2, minutes=3, seconds=4)
	dts[7] = adjust(dtNow, days=1, hours=2, minutes=3, seconds=4)
	testDateTimeStrip(dts)
	print()
	
def test2 ():
	dts = [None]*8 
	dtNow = datetime.datetime.now()
	dts[0] = dtNow
	dts[1] = adjust(dtNow, days=-1)
	dts[2] = adjust(dtNow, hours=-2)
	dts[3] = adjust(dtNow, minutes=-3)
	dts[4] = adjust(dtNow, seconds=-4)
	dts[5] = adjust(dtNow, days=-1, seconds=-4)
	dts[6] = adjust(dtNow, hours=-2, minutes=-3, seconds=-4)
	dts[7] = adjust(dtNow, days=-1, hours=-2, minutes=-3, seconds=-4)
	testDateTimeStrip(dts)
	print()

def getTestDeltas (url):
	with urllib.request.urlopen(url) as src:
		html = lxml.html.parse(src)
		listing = ReportListing(html)
		dateTimes = listing.getDateTimes()
		deltas = []
		for i in range(0, len(dateTimes)-1):
			delta = dateTimes[i] - dateTimes[i+1]
			deltas.append(delta)
		return deltas


def testGetStartTime ():
	url = "http://mis.ercot.com/misapp/GetReports.do?reportTypeId=12331&reportTitle=DAM%20Settlement%20Point%20Prices&showHTMLView=&mimicKey"
	deltas = getTestDeltas(url)
	interval = IntervalCalculator.getInterval(deltas)
	if interval == IntervalEnum.DAILY:
		startTime = IntervalCalculator._getDailyStartTime(deltas)
		sStartTime = time.strftime("%H:%M:%S", startTime)
		print("startTime={}".format(sStartTime))

if __name__ == '__main__':
	# testGetStartTime()
	testDateTimeStrip()

