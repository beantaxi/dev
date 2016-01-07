import lxml.html
import os.path
from ExtractListing import ExtractListing
from api import ExtractFilename


def testParseExtractFilename ():
	filename = "cdr.00012300.0000000000000000.20151207.181016405.LMPSROSNODENP6788_20151207_181011_csv.zip"
	ef = ExtractFilename(filename)
	print(ef.filename)
	print(ef.reportId)
	print(ef.datetime)

def testParseExtractInfo ():
	path = "/data/downloads/listings/12300.html"
	print(ExtractListing.XPATH)
	html = lxml.html.parse(path)
	els = html.xpath(ExtractListing.XPATH)
	for el in els:
		print(el)

def testCheckForExtracts ():
	path = "/data/downloads/listings/12300.html"
	homeFolder = "/data/downloads"
	listing = ExtractListing(path)
	for dt, info in listing.extractInfo.items():
		sDate = dt.strftime('%Y%m%d')
		folder = os.path.join(homeFolder, sDate)
		path = os.path.join(folder, info['filename'])
		print('{} {}'.format(path, os.path.isfile(path)))
	
		
if __name__ == '__main__':
#	testParseExtractFilename()
#	testParseExtractInfo()
	testCheckForExtracts()

