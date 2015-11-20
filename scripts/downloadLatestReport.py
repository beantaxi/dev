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
	
def downloadLatestReport (urlReportListing, format='csv'):
	(urlReport, filename) = getReportUrlAndFilename(url, format)
	downloadFolder = '/tmp/downloads/ercot'
	downloadPath = os.path.join(downloadFolder, filename)
	sUrlReport = urllib.parse.urlunparse(urlReport)
	print(sUrlReport)
	ctx = createContext()
	ins = urllib.request.urlopen(url, context=ctx)
	s = ins.read()
	print(s)
#	with urllib.request.urlopen(sUrlReport, context=ctx) as src, open(downloadPath, "w") as dst:
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


def getReportUrlAndFilename (urlReportListing, format='csv'):
	(xpathFilename, xpathUrl) = getXPaths(format)
	sUrl = urllib.parse.urlunparse(urlReportListing)
	ctx = createContext()
	src = urllib.request.urlopen(sUrl, context=ctx)
	html = lxml.html.parse(src)
	filename = html.xpath(xpathFilename)[0].strip()
	sRelativeReportUrl = html.xpath(xpathUrl)[0].strip()
	(path, query) = sRelativeReportUrl.split('?')
	urlReport = urlReportListing._replace(path=path, query=query)
	return (urlReport, filename)




if __name__ == "__main__":
	arg = sys.argv[1]
	url = ExtractTable.getReportUrl(arg)
	downloadLatestReport(url)

# reportName = argv[1]
# url = createErcotUrl.createErcotUrl(reportName)
# print("url=" + url)
# html = lxml.html.parse(url).getroot()
# els = html.cssselect('.labelOptional_ind')
# for el in els:
# 	if el.text.endswith('_csv.zip'):
# 		destPath = el.text
# 		destPath = os.path.join("/tmp/downloads", destPath)
# 		href = el.getparent().getchildren()[3].xpath('div/a/@href')[0]
# 		(path, query) = href.split('?')
# 		parts = urllib.parse.urlparse(url)
# 		dataUrl = urllib.parse.urlunparse(parts._replace(path=path, query=query))
# 		print("dataUrl=" + dataUrl);
# 		print("path=" + path);
# 		urllib.request.urlretrieve(dataUrl, destPath)
# 		print("Downloaded " + destPath)
# 		with zipfile.ZipFile(destPath) as z:
# 			z.extractall("/tmp/downloads")
# 		break
