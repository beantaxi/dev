import datetime
import urllib.request
import io
import lxml.html
import shutil

url = "http://www.ercot.com/content/cdr/contours/rtmLmpHg.html"
urlroot = "http://www.ercot.com/content/cdr/contours"
xpath = "//img[@usemap='#CONTOUR_IMAGE_MAP']/@src"

URL_Kml = "http://www.ercot.com/content/cdr/contours/rtmLmpHg.kml"
# kmlFilename = datetime.datetime.now().strftime("/tmp/ercot-%Y%m%d-%H%M.kml")


def createFilenameBase ():
	s = datetime.datetime.now().strftime("%Y%m%d-%H%M")
	return s


def createImageFileName (base):
	s = base + ".png"
	return s


def createKmlFileName (base):
	s = base + ".kml"
	return s


def createImageUrl (imageName):
	imageUrl = urlroot + "/" + imageName
	return imageUrl


def downloadKml (kmlFilename):
	response = urllib.request.urlopen(URL_Kml)
	print('Opening file ...')
	outPath = '../contourMaps/' + kmlFilename
	print('Saving ' + URL_Kml + ' to ' + outPath + ' ...')
	outFile = open(outPath, 'wb')
	shutil.copyfileobj(response, outFile)


def getHtml ():
	doc = lxml.html.parse(url)
	root = doc.getroot()
	return root


def getImgSrc (html):
	imgSrc =	html.xpath(xpath)[0]
	return imgSrc


def saveFile (imageSrc, imageFileName):
	urllib.request.urlretrieve(imageSrc, '../contourMaps/' + imageFileName)


def test ():
	print("Hello!")
	
	html = getHtml()
	print("Retrieved html ...")

	imgsrc = getImgSrc(html)
	print(imgsrc)
#	print("Img src = " + imgsrc + " ...")

	imageUrl = createImageUrl(imgsrc)
	print("Image URL = " + imageUrl + " ...")


	filenameBase = createFilenameBase()

	imageFileName = createImageFileName(filenameBase)
	print("File name = " + imageFileName + " ...")

	print("Saving " + imageUrl + " to " + imageFileName + " ...")
	saveFile(imageUrl, imageFileName)

	print("Saving KML ...")
	kmlFilename = createKmlFileName(filenameBase)
	downloadKml(kmlFilename)

#	print("Done")
	

test()
