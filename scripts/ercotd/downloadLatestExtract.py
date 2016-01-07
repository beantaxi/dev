import sys
import lxml.html
import os.path
import shutil
import ssl
import urllib
import urllib.parse
import urllib.request
import zipfile
# import createErcotUrl
import ExtractTable
import _utils

xpathCsvFilename = "//tr[td[@class='labelOptional_ind'][text()[contains(., '_csv')]]]/td[1]/text()"
xpathCsvUrl =      "(//tr[td[@class='labelOptional_ind'][text()[contains(., '_csv')]]])[1]/td[4]/div/a/@href"
xpathXmlFilename = "//tr[td[@class='labelOptional_ind'][text()[contains(., '_xml')]]]/td[1]/text()"
xpathXmlUrl =      "(//tr[td[@class='labelOptional_ind'][text()[contains(., '_xml')]]])[1]/td[4]/div/a/@href"

def createContext ():
	certPath = "/home/chrissy/.ssh/ercot-mis-client-and-pk.pem"
	ctx = _utils.createContext(certPath)
	return ctx
	
def downloadLatestExtract (urlExtractListing, format='csv'):
	(urlExtract, filename) = getExtractUrlAndFilename(url, format)
	downloadFolder = '/tmp/downloads/ercot'
	downloadPath = os.path.join(downloadFolder, filename)
	sUrlExtract = urllib.parse.urlunparse(urlExtract)
	print(sUrlExtract)
	ctx = createContext()
	ins = urllib.request.urlopen(url, context=ctx)
	s = ins.read()
	print(s)
#	with urllib.request.urlopen(sUrlExtract, context=ctx) as src, open(downloadPath, "w") as dst:
#		shutil.copyfileobj(src, dst)

def getXPaths (sFormat):
	if sFormat == 'csv':
		xpathFilename = xpathCsvFilename
		xpathUrl = xpathCsvUrl
	elif sFormat == 'xml':
		xpathFilename = xpathXmlFilename
		xpathUrl = xpathXmlUrl
	else:
		raise Exception("Unknown sFormat: " + str(sFormat))
	return (xpathFilename, xpathUrl)


def getExtractUrlAndFilename (urlExtractListing, format='csv'):
	(xpathFilename, xpathUrl) = getXPaths(format)
	sUrl = urllib.parse.urlunparse(urlExtractListing)
	ctx = createContext()
	src = urllib.request.urlopen(sUrl, context=ctx)
	html = lxml.html.parse(src)
	filename = html.xpath(xpathFilename)[0].strip()
	sRelativeExtractUrl = html.xpath(xpathUrl)[0].strip()
	(path, query) = sRelativeExtractUrl.split('?')
	urlExtract = urlExtractListing._replace(path=path, query=query)
	return (urlExtract, filename)




if __name__ == "__main__":
	arg = sys.argv[1]
	url = ExtractTable.getExtractUrl(arg)
	downloadLatestExtract(url)
