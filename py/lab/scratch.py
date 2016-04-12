import sys

try:
	raise Exception("some message")
except Exception as ex:
	print((str(ex) + "\r").encode('utf-8'))

