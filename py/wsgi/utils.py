import traceback

def tracebackAsLines (tb):
	lines = []
	for tbLine in traceback.extract_tb(tb):
		(file, ln, fn, msg) = tbLine
		s = "at {}:{} in {}() {}".format(file, ln, fn, msg)
		lines.append(s)
	return lines
