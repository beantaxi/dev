################################################################################
#
# Download and parse a extract list (url), and print the URL for the latest extract
# (CSV version).
#
################################################################################

import lxml.html
import urllib.parse

# file = '/home/chrissy/work/euclid/scripts/reportListing.html'
file = 'http://mis.ercot.com/misapp/GetReports.do?reportTypeId=12328&reportTitle=DAM+Hourly+LMPs'

xpathCsvFilename = "//tr[td[@class='labelOptional_ind'][text()[contains(., '_csv')]]]/td[1]/text()"
xpathCsvUrl =      "(//tr[td[@class='labelOptional_ind'][text()[contains(., '_csv')]]])[1]/td[4]/div/a/@href"
xpathXmlFilename = "//tr[td[@class='labelOptional_ind'][text()[contains(., '_csv')]]]/td[1]/text()"
xpathXmlUrl =      "(//tr[td[@class='labelOptional_ind'][text()[contains(., '_xml')]]])[1]/td[4]/div/a/@href"


def getExtractUrl (extractListingUrl, extractRelativeUrl):
	# Split up the relativeUrl from the listing, into path and query
	(path, query) = extractRelativeUrl.split('?')
	# Break the extract listing URL up into its parts, then replace the old path and query with the new
	parts = urllib.parse.urlparse(extractListingUrl)
	extractUrl = urllib.parse.urlunparse(parts._replace(path=path, query=query))
	return extractUrl
	
html = lxml.html.parse(file)
filename = html.xpath(xpathFilename)[0].strip()
relativeUrl = html.xpath(xpathUrl)[0].strip()
extractUrl = getExtractUrl(file, relativeUrl)

print(filename)
# print(lxml.html.tostring(url, pretty_print=True))
print(extractUrl)

#for el in els:
#	if type(el).__name__ == "_ElementUnicodeResult":
#		print(el)
#	else:
#		print(lxml.html.tostring(el, pretty_print=True))
