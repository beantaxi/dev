import lxml.html

if __name__ == '__main__':
	html = lxml.html.parse('scratch.html')
	xpath = "/html/body/table//td"
	els = html.xpath(xpath)
	print("{} hit(s)".format(len(els)))

