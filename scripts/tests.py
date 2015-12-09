import lxml.html
import _utils

def testParseExtractFilename ():
	filename = "cdr.00012300.0000000000000000.20151207.181016405.LMPSROSNODENP6788_20151207_181011_csv.zip"
	extractFilename = _utils.ExtractFilename(filename)
	print(extractFilename)


if __name__ == '__main__':
	testParseExtractFilename()

