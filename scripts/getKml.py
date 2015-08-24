import datetime
import shutil
import urllib.request

URL = "http://www.ercot.com/content/cdr/contours/rtmLmpHg.kml"
filename = datetime.datetime.now().strftime("/tmp/ercot-%Y%m%d-%H%M.kml")

print('Getting response ...')
response = urllib.request.urlopen(URL)
print('Opening file ...')
outFile = open(filename, 'wb')
print('Saving file ...')
shutil.copyfileobj(response, outFile)

print("Done")
