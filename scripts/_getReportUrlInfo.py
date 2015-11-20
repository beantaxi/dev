import sys;
import urllib.parse
import ExtractTable

def parse (url):
	parts = urllib.parse.urlparse(url)
	q = urllib.parse.parse_qs(parts.query)
	id = q['reportTypeId'][0]
	name = q['reportTitle'][0]
	reportInfo = ExtractTable.ReportInfo(id, name, url)
	return reportInfo

if __name__ == "__main__":
	print("I'm a main program!")
	sUrl = sys.argv[1]
	print(sUrl)
	info = getInfo(sUrl)
	print("{},\"{}\"".format(info['id'], info['name']))
