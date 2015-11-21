import argparse
import datetime
import lxml.html
import urllib.request
import X
from collections import OrderedDict
from IntervalCalculator import IntervalCalculator
from TimeDelta2 import TimeDelta2
import _utils

class ExtractListing:
	XPATH = "//tr[td[1][@class='labelOptional_ind'][text()[contains(., '_csv.zip')]]]/td[1]/text() | //tr[td[1][@class='labelOptional_ind'][text()[contains(., '_csv.zip')]]]/td[4]//div/a/@href"
	def __init__ (self):
		pass

	@staticmethod
	def getDateTime (extractFilename):
		parts = extractFilename.split('.')
		sDate = parts[3]
		sTime = parts[4]
		sDateTime = sDate + sTime
		sDateTimeFormat = '%Y%m%d%H%M%S%f'
		dt = datetime.datetime.strptime(sDateTime, sDateTimeFormat)
		return dt
	

	@staticmethod
	def isDailyExtract (extractDateTimes):
		pass
#		Zero time out on each
#		Compare dates

	@classmethod
	def parseExtractInfo (cls, html):
		results = html.xpath(cls.XPATH)
		nRows = int(len(results)/2)
		print("nRows={}".format(nRows))
		extracts = {}
		for i in range(0, nRows):
			filename = results[i*2].strip()
			url = results[i*2+1].strip()
			datetime = ExtractListing.getDateTime(filename)
			extracts[datetime] = {'filename': filename, 'url': url}
		od = OrderedDict()
		for key in sorted(extracts, reverse=True):
			od[key] = extracts[key]
		return od
			



	def getDateTimes (self):
		dateTimes = [ExtractListing.getDateTime(s) for s in self.getExtractFilenames()]
		return dateTimes
		
	def getExtractFilenames (self):
		xpathExtractFilenames = "//tr[td[@class='labelOptional_ind'][text()[contains(., '_csv.zip')]]]/td[1]/text()"
		extractFilenames = self.html.xpath(xpathExtractFilenames)
		return extractFilenames

	def getExtractUrls (self):
		xpathExtractFilenames = "//tr[td[@class='labelOptional_ind'][text()[contains(., '_csv.zip')]]]/td[1]/text()"
		extractFilenames = self.html.xpath(xpathExtractFilenames)
		return extractFilenames

	def load (self, url):
		with urllib.request.urlopen(url) as src:
			self.html = lxml.html.parse(src)
			self.parseExtractInfo()

if __name__ == '__main__':
	argparse = argparse.ArgumentParser()
	argparse.add_argument('url')
	argparse.add_argument('-dl', '--download-latest', action='store_true', dest='downloadLatest')
	argparse.add_argument('-i', '--show-intervals', action='store_true', dest='showIntervals')
	argparse.add_argument('-ls', '--list', action='store_true', dest='list')
	args = argparse.parse_args()
	url = args.url
	listing = ExtractListing()
	listing.load(url)
	if args.showIntervals:
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
	elif args.downloadLatest:
		print("STUFFFFF!")
	elif args.list:
		for filename in listing.getExtractFilenames():
			print(filename)

