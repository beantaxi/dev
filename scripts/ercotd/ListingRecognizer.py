from enum import Enum
import lxml.html
import os
import urllib.request
import X

class ListingEnum(Enum):
	Extracts = 1
	Report = 2
	UnknownErcot = 100
	NonErcot = 999

class ListingRecognizer:
	XP_Ercot = "/html/body/form/input[@value='https://mis.ercot.com:443/misapp/']"
#	XP_Ercot = "/html/body/form/input"
	XP_ExtractListing = "/html/body/form/table/tr[2]//td[@class='labelOptional_ind'][text()[starts-with(., 'cdr')]]"
	XP_ReportListing = "/html/body/form/table/tr[2]//td[@class='labelOptional_ind'][text()[starts-with(., 'rpt')]]"

	@classmethod
	def recognizeListing (cls, url):
		with urllib.request.urlopen(url) as src:
			html = lxml.html.parse(src)
		if not html.xpath(cls.XP_Ercot)):
			r = ListingEnum.NonErcot
		print('ERCOT!' if isErcot else "I don't think this is Ercot")
		# Check for cdrs
		if len(html.xpath(cls.XP_ExtractListing)):
			print("Extract Listing")
		# Check for rpts
		if len(html.xpath(cls.XP_ReportListing)):
			print("Report Listing")

if __name__ == '__main__':
	if 'url' in os.environ.keys():
		url = os.environ['url']
		ListingRecognizer.recognizeListing(url)

