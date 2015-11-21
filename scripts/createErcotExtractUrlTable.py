import sys;
import urllib.parse

for line in sys.stdin:
	line = line.strip()
	url = urllib.parse.urlparse(line)
	q = urllib.parse.parse_qs(url.query)
	id = q['extractTypeId'][0]
	name = q['extractTitle'][0]
	print("{},\"{}\",\"{}\"".format(id, name, line))



