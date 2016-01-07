import http.cookiejar
import shutil
import ssl
import urllib.request
import _utils

#url = "https://mis.ercot.com/misapp/GetReports.do?reportTypeId=11485&noOfDaysofArchive=3&reportTitle=LMPs%20by%20Electrical%20Bus&showHTMLView=undefined&mimicKey="
url = "https://mis.ercot.com/misdownload/servlets/mirDownload?mimic_duns=0799701548000&doclookupId=496571551"

def installOpener (certPath, caPath):
	httpsProcessor = _utils.createHttpsProcessor(certPath=certPath, caPath=caPath)
	cookieProcessor = _utils.createCookieProcessor()
	opener = urllib.request.build_opener(httpsProcessor, cookieProcessor)
	urllib.request.install_opener(opener)

certPath = "/home/chrissy/.ssh/ercot-mis-client-and-pk.pem" 
caPath = "/home/chrissy/.ssh/ercot-mis-ca.pem"
downloadPath = '/tmp/download-new.zip'


def method1 ():
	ctx = _utils.createContext(certPath=certPath, caPath=caPath)
	with urllib.request.urlopen(url, context=ctx) as src, open(downloadPath, 'wb') as dst:
		shutil.copyfileobj(src, dst)

def method2 ():
	installOpener(certPath=certPath, caPath=caPath)
	with urllib.request.urlopen(url) as src, open(downloadPath, 'wb') as dst:
		shutil.copyfileobj(src, dst)
	
if __name__ == "__main__":
	method2()
