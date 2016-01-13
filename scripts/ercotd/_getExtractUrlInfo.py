import sys;
import urllib.parse
import api
from ExtractTable import ExtractInfo

if __name__ == "__main__":
	sUrl = sys.argv[1]
	print(sUrl)
	info = getInfo(sUrl)
	print("{},\"{}\"".format(info['id'], info['name']))
