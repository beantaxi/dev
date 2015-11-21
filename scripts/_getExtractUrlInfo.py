import sys;
import urllib.parse
import ExtractTable

def parse (url):
	parts = urllib.parse.urlparse(url)
	q = urllib.parse.parse_qs(parts.query)
	id = q['extractTypeId'][0]
	name = q['extractTitle'][0]
	extractInfo = ExtractTable.ExtractInfo(id, name, url)
	return extractInfo

if __name__ == "__main__":
	print("I'm a main program!")
	sUrl = sys.argv[1]
	print(sUrl)
	info = getInfo(sUrl)
	print("{},\"{}\"".format(info['id'], info['name']))
