import lxml.html

file = '/home/chrissy/work/euclid/scripts/reportListing.html'
xpath = "(//tr[td[@class='labelOptional_ind'][text()[contains(., '_csv')]]])[1]"



# /td[5]
# /div/a/@href

html = lxml.html.parse(file)
o = html.xpath(xpath)[0]

if type(o).__name__ == "_ElementUnicodeResult":
	print(o)
elif type(o).__name__ == "list":
	print(o)
else:
	print(lxml.html.tostring(o, pretty_print=True))

# print(lxml.html.tostring(url, pretty_print=True))
print(url)

