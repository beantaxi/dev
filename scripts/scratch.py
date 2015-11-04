import colorama
import datetime
import logging
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

def modTo5Minutes (dt):
	tOrig = dt.time();
	h = 0
	m = tOrig.minute % 5
	s = tOrig.second
	t = datetime.time(h, m, s)
	logging.debug("{} - {} {}".format(str(tOrig), str(m), str(s)))
	return t

def testDateTimeStrip ():
	url = "https://mis.ercot.com/misapp/GetReports.do?reportTypeId=11485&noOfDaysofArchive=3&reportTitle=LMPs%20by%20Electrical%20Bus&showHTMLView=undefined&mimicKey="
	with urllib.request.urlopen(url) as src:
		html = lxml.html.parse(src)
	listing = ReportListing(html)
	times = [modTo5Minutes(dt) for dt in listing.getDateTimes()]
	(min, max, avg) = _utils.timeMinMaxAvg(times)
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

def testAskDatetime ():
	prompt = "Time? [HH:MM] "
	fmt = "%H:%M"
	dt = _utils.askDatetime(prompt, fmt)
	print("dt=" + str(dt))	

def testAskTime ():
	prompt = "Time? [HH:MM] "
	fmt = "%H:%M"
	t = _utils.askTime(prompt, fmt)
	print("time=" + str(t))	

def testAskMultiChoice ():
	promptFmt = "Would you like to choose the rounded Mi{0}n{1}, Ma{0}x{1}, {0}A{1}vg, or {0}O{1}ther?"
	prompt = promptFmt.format(colorama.Fore.BLUE + colorama.Style.BRIGHT, colorama.Style.RESET_ALL)
	choices = 'NXAO'
	choice = _utils.askMultiChoice(prompt, choices, 'N')
	print("choice=" + choice)
	
def testCrons ():
	t = datetime.datetime.now().time()
	print("t=" + str(t))
	dailyCron = _utils.createDailyCron(t)
	print("dailyCron=" + dailyCron)

def testRounding ():
	# dt = datetime.datetime.now()
	dt = datetime.time(19, 26, 55, 900000)
	print(dt)
	delta = datetime.timedelta(seconds=1)
	dtFloor = _utils.floorTime(dt, delta)
	dtCeil = _utils.ceilTime(dt, delta)
	dtRound = _utils.roundTime(dt, delta)
	print("dtCeil=" + str(dtCeil))
	print("dtFloor=" + str(dtFloor))
	print("dtRound=" + str(dtRound))

if __name__ == '__main__':
	# testGetStartTime()
	# testDateTimeStrip()
	testRounding()
	# testAskMultiChoice()
	# testAskDatetime()
	# testAskTime()
	# testCrons()
