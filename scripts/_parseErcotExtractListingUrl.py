import sys;
import urllib.parse

def parse (sUrl):
	url = urllib.parse.urlparse(sUrl)
	q = urllib.parse.parse_qs(url.query)
	id = q['extractTypeId'][0]
	name = q['extractTitle'][0]
	info = {'id': id, 'name': name, 'url': url}
	return info

if __name__ == "__main__":
	print("I'm a main program!")
	sUrl = sys.argv[1]
	print(sUrl)
	info = getInfo(sUrl)
	print("{},\"{}\"".format(info['id'], info['name']))
