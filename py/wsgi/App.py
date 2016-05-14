# import urllib.parse

import imp
import sys
import traceback
import jinja2
from wsgi import utils
from wsgi import DateRangeParser
from wsgi import GeneralClientEx
from wsgi import InvalidMethodEx
from wsgi import extracts

def createAndEnhanceModule (moduleName, path):
	module = imp.load_source(moduleName, path)
	module.validateMethod = validateMethod
	return module


def enrichModule (module):
	module.validateMethod = validateMethod
	# import exceptions


def execModule (module):
	attrs1 = set(dir(module))
	module.exec()
	attrs2 = set(dir(module))
	newAttrs = [el for el in attrs2 if el not in attrs1 and el != '__builtins__']
	args = {}
	for attr in newAttrs:
		val = getattr(module, attr)
		if not inspect.isfunction(val) and not inspect.isclass(val):
			args[attr] = getattr(module, attr)
	return args


def execTemplate (templatePath, args):
	jloader = jinja2.FileSystemLoader(os.getcwd())
	jenv = jinja2.Environment()
	templateName = os.path.basename(templatePath)
	jtemplate = jloader.load(jenv, templateName)
	s = jtemplate.render(args)
	return s 


def getModulePath (env):
	path = env['PATH_INFO']
	moduleFilename = path[1:].lpartition('/')[0] + '.py'
	modulePath = os.path.join(os.getcwd(), moduleFilename)
	return modulePath


def getTemplatePath (env):
	path = env['PATH_INFO']
	templateFilename = path[1:].lpartition('/')[0] + '.pyp'
	templatePath = os.path.join(os.getcwd(), templateFilename)
	return templatePath


def validateMethod (method, methods):
	if not method in methods:
		raise InvalidMethodEx(method, methods)


class Response:
	def __init__ (self):
		self.text = ""


class Application ():
	def __init__ (self, env, start_response):
		print("os.getcwd()={}".format(os.getcwd()))
		self.env = env
		self.startResponse = start_response
		self.response = Response()
		try:
			modulePath = getModulePath(env)
			module = MagicLoader.getModule(fullPath)
			enrichModule(module)
			args = execModule(module)
			templatePath = getTemplatePath(env)
			self.response.text = execTemplate(templatePath, args)

# 			path = env['PATH_INFO']
# 			parts = path.split('/')
# 			moduleStub = parts[1]	
# #			moduleName = 'wsgi.{}'.format(moduleStub)
# #			modulePath = 'wsgi/{}.py'.format(moduleStub)
# #			module = createAndEnhanceModule(moduleName, modulePath)
# 			filename = '{}.py'.format(moduleStub)
# 			args = {}
# 			g = {}
# 			g['validateMethod'] = validateMethod
# 			g['app'] = self 
# 			g['args'] = args
# 			with open(filename) as f:
# 				code = compile(f.read(), filename, 'exec')
# 				exec(code, g)
# #			module.validateMethod = validateMethod
# #			module.app = self
# #			args = []
# #			module.args = args
# #			validate = getattr(module, 'validate')
# #			generatePage = getattr(module, 'generatePage')
# #			validate(self)
# 			self.startResponse('200 OK', [('Content-type', 'text/html')])
# 			jloader = jinja2.FileSystemLoader('/home/ubuntu/dev/py/wsgi/templates')
# 			jenv = jinja2.Environment()
# 			jtemplate = jloader.load(jenv, 'extracts.pyp')
# 			self.response.text = jtemplate.render(args)
		except GeneralClientEx as ex:
			print(ex)
			headers = [
				('Content-type', 'text/plain'),
				('Warning', ex.getWarningHeaderValue())
			]
			self.startResponse('400 Oops', headers, sys.exc_info())
			self.response.text = str(ex)
		except InvalidMethodEx as ex:
			print(ex)
			headers = [
				("Content-type", "text/plain"),
				("Allow", ex.getAllowHeaderValue())
			]
			self.startResponse("405", headers, sys.exc_info())
			self.response.text = str(ex) 
		except Exception as ex:
			traceback.print_exc()
			headers = [
				("Content-type", "text/plain")
			]
			self.startResponse("500", headers, sys.exc_info())
			self.response.text = "An error has occured on the server."
#	extractId = parts[2]
#	datestr = parts[3]
	
#	try:
#		utils.validateRequestMethod(env, ['GET'])
#		dtRange = dateRangeParser.getDateRange(datestr)
#		(dtStart, dtEnd) = dtRange
#		resp += "<table>"
#		resp += "<tr> <td>extractId</td> <td>{}</td> </tr>".format(extractId)
#		resp += "<tr> <td>datestr</td> <td>{}</td> </tr>".format(datestr)
#		resp += "<tr> <td>dtStart</td> <td>{}</td> </tr>".format(dtStart)
#		resp += "<tr> <td>dtEnd</td> <td>{}</td> </tr>".format(dtEnd)
#		resp += "</table>"
#	except Exception as ex:
#		headers = [('Content-type', 'text/plain')]
#		start_response('500 Oops', headers, sys.exc_info())
#		resp = ""
#		resp += str(ex) + '\r'
#		resp += "\r"
#		(exType, exInst, tb) = sys.exc_info()
#		lines = utils.tracebackAsLines(tb)
#		for line in lines:
#			resp += line + "\r"
	def __iter__ (self):
		yield self.response.text.encode('utf-8')


	def generatePage (self):
		path = self.env['PATH_INFO']
		parts = path.split('/')
		extractId = parts[2]
		datestr = parts[3]
		dtRange = DateRangeParser.getDateRange(datestr)
		(dtStart, dtEnd) = dtRange
		args = {
			'extractId': extractId,
			'dtStart': dtStart,
			'dtEnd': dtEnd
		}

		jloader = jinja2.FileSystemLoader('/home/ubuntu/dev/py/wsgi/templates')
		jenv = jinja2.Environment()
		jtemplate = jloader.load(jenv, 'extracts.pyp')
		self.response.text = jtemplate.render(args)

	def dumpParts (self):
		for i, part in enumerate(parts):
			self.response.text += "{} => {}<br>".format(i, part)

	def validateParts (self):
		path = self.env['PATH_INFO']
		parts = path.split('/')
		if len(parts) < 4 or len(parts[0]) > 0 or not DateRangeParser.isValid(parts[3]):
			msg = "URL path must be of form /extract/[extractId]/YYMMDD or /extract/[extractId]/YYMMDD-YYMMDD"
			raise GeneralClientEx(msg)
