import argparse
import datetime
import lxml.html
import urllib.request
import X
from IntervalCalculator import IntervalCalculator
from TimeDelta2 import TimeDelta2
import _utils

class ReportListing:
	def __init__ (self, html):
		self.html = html

	@staticmethod
	def getDateTime (reportFilename):
		parts = reportFilename.split('.')
		sDate = parts[3]
		sTime = parts[4]
		sDateTime = sDate + sTime
		sDateTimeFormat = '%Y%m%d%H%M%S%f'
		dt = datetime.datetime.strptime(sDateTime, sDateTimeFormat)
		return dt
	

	@staticmethod
	def isDailyReport (reportDateTimes):
		pass
#		Zero time out on each
#		Compare dates

	def getDateTimes (self):
		dateTimes = [ReportListing.getDateTime(s) for s in self.getReportFilenames()]
		return dateTimes
		
	def getReportFilenames (self):
		xpathReportFilenames = "//tr[td[@class='labelOptional_ind'][text()[contains(., '_csv.zip')]]]/td[1]/text()"
		reportFilenames = self.html.xpath(xpathReportFilenames)
		return reportFilenames

if __name__ == '__main__':
	argparse = argparse.ArgumentParser()
	argparse.add_argument('url')
	args = argparse.parse_args()
	url = args.url
	with urllib.request.urlopen(url) as src:
		html = lxml.html.parse(src)
	listing = ReportListing(html)
	dateTimes = listing.getDateTimes()
	nLoop = min(10, len(dateTimes))
	dtLast = None
	for i in range(0, nLoop):
		dtCurr = dateTimes[i]
		if not dtLast:
			sDelta = "--"
		else:
			delta = dtLast-dtCurr
			sDelta = TimeDelta2.toString(delta) 
#		print('{:>32}{}'.format(dtCurr, sDelta))
		print('{0:50}{1:>32}'.format(str(dtCurr), sDelta))
		dtLast = dtCurr

	deltas = _utils.getDeltas(dateTimes, descending=True)
	for delta in [delta.total_seconds() for delta in deltas]:
		print(delta)
	interval = IntervalCalculator.getInterval(deltas)
	print("interval=" + str(interval))

