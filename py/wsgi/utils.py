import traceback

def tracebackAsLines (tb):
	lines = []
	for tbLine in traceback.extract_tb(tb):
		(file, ln, fn, msg) = tbLine
		s = "at {}:{} in {}() {}".format(file, ln, fn, msg)
		lines.append(s)
	return lines


def validateRequestMethod (env, methods=['GET']):
	if isinstance(methods, str):
		methods = [methods]
	method = env['REQUEST_METHOD']
	if not method in methods:
		msg = "Invalid method '%s'. Method must be one of %s" % (method, methods)
		raise Exception(msg)
	return True

