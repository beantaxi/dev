import lxml.html
import sys

xpath = "//img[@usemap='#CONTOUR_IMAGE_MAP']/@src"

doc = lxml.html.parse(sys.stdin)
html = doc.getroot()
imgSrc =	html.xpath(xpath)[0]
print(imgSrc)

