import os.path
import base64

validateMethod('get')
datestr = http.path[1]
imgPath = "/home/chrissy/dev/py/wsgi/img/{}-0000.png".format(datestr)
flag = os.path.isfile(imgPath)
with open(imgPath, 'rb') as f:
	data = f.read()

setContentType('image/png')
_ = data
#_ = """
#path = {{ http.path }}
#path[0] =  {{http.path[0]}}
#path[1] =  {{http.path[1]}}
#imgPath = {{ imgPath }}
#flag = {{ flag }}
#data = {{ data }}
#OK
#"""
