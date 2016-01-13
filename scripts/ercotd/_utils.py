import colorama
from datetime import datetime
from datetime import time
from datetime import timedelta
import distutils.util
import logging
import http.cookiejar
import os.path
import shutil
import ssl
import syslog
import sys
import urllib.request
import zipfile

class _syslog:
	@classmethod
	def debug (cls, msg):
		syslog.syslog(syslog.LOG_DEBUG, msg)
	
	@classmethod
	def error (cls, msg):
		syslog.syslog(syslog.LOG_ERR, msg)

	@classmethod
	def info (cls, msg):
		syslog.syslog(syslog.LOG_INFO, msg)


def adjust (dt, weeks=0, days=0, hours=0, minutes=0, seconds=0, milliseconds=0, microseconds=0):
	localVars = dict(locals())
	del localVars['dt']
	td = timedelta(**localVars)
	dtNew = dt + td
	return dtNew


def ask (prompt, default=None):
	if default:	
		sDefault = str(default)
		prompt = "{} [{}]".format(prompt, sDefault)
	if not prompt.endswith(' '):
		prompt = prompt + ' '
	done = False
	while not done:
		s = input(prompt)
		if s:
			done = True
		elif default:
			s = default
			done = True
	return s


def askDatetime (prompt, fmt):
	done = False
	while not done:
		try:
			sDatetime = input(prompt)
			dt = datetime.strptime(sDatetime, fmt)
			done = True
		except ValueError:
			print(colorama.Fore.RED + "Please enter a valid date/time in the proper format" + colorama.Style.RESET_ALL)
	return dt


def askTime (prompt, fmt="%H:%M:%S"):
	done = False
	while not done:
		try:
			sTime = input(prompt)
			t = datetime.strptime(sTime, fmt).time()
			done = True
		except ValueError:
			print(colorama.Fore.RED + "Please enter a valid time in the proper format" + colorama.Style.RESET_ALL)
	return t


def askYesNoChoice (prompt, default=None):
	if default == None:	
		prompt = prompt + (" (y/n) ")
	else:
		sDefault = str(default)
		default = distutils.util.strtobool(sDefault)
		if default == True:
			prompt = prompt + (" (Y/n) ")
		else:
			prompt = prompt + (" (y/N) ")
	choice = None
	while choice == None:
		try:
			sChoice = input(prompt)
			if sChoice == "" and default is not None:
				sChoice = str(default)
			choice = distutils.util.strtobool(sChoice)
		except ValueError:
			print("Invalid choice: " + sChoice)
	return choice	


def askMultiChoice (prompt, charChoices, default=None):
	charChoices = charChoices.lower()
	sChoices = ''.join(list(charChoices))
	if default:
		sChoices = sChoices.replace(default.lower(), default.upper())
	prompt = "{} [{}]: ".format(prompt, sChoices)
	done = False
	while not done:
		choice = input(prompt).lower()
		if len(choice) == 0 and default:
			choice = default.lower()
		if len(choice) != 1:
			print("Please enter a single character")
		elif choice[0] not in charChoices:
			print("Please enter a valid choice")
		else:
			done = True
	return choice
			
				

def createContext (clientCertPath, caCertPath):
	ctx = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
	ctx.load_cert_chain(clientCertPath)
	ctx.load_verify_locations(caCertPath)
	return ctx

def createCookieProcessor (cookieJar=None):
	if not cookieJar:
		cookieJar = http.cookiejar.CookieJar()
	cookieProcessor = urllib.request.HTTPCookieProcessor(cookieJar)
	return cookieProcessor

def createDailyCron (tStart):
	h = tStart.hour
	m = tStart.minute
	fmt = "{} {} * * *"
	cron = fmt.format(m, h)
	return cron

def createHourlyCron (tStart):
	m = tStart.minute
	fmt = "{} * * * *"
	cron = fmt.format(m)
	return cron

def createMinuteCron (tStart, mInterval):
	seq = range(0, 60//mInterval)  
	minutes = [str(tStart.minute + m*mInterval) for m in seq]
	sMinutes = ','.join(minutes)
	fmt = "{} * * * *"
	cron = fmt.format(sMinutes)
	return cron

def createHttpsHandler (clientCertPath, caCertPath):
	ctx = createContext(clientCertPath=clientCertPath, caCertPath=caCertPath)
	httpsHandler = urllib.request.HTTPSHandler(context=ctx)
	return httpsHandler

def getCertPath (certName):
	if sys.platform == 'linux':
		homeFolder = os.path.expanduser('~')
		certFolder = os.path.join(homeFolder, '.ssh')
		certPath = os.path.join(certFolder, certName)
	else:
		raise("{} is not supported at this time".format(sys.platform))
	return certPath
	

def roundTime (t, delta=timedelta(minutes=1)):
	seconds = t.hour*3600 + t.minute*60 + t.second
	deltaSeconds = delta.seconds
	roundedSeconds = (seconds + deltaSeconds//2) // deltaSeconds * deltaSeconds
	h, extra = divmod(roundedSeconds, 3600)
	m, s = divmod(extra, 60)
	roundedTime = time(h, m, s)
	return roundedTime

def timeMinMaxAvg (times):
	min = max = avg = None
	totalSeconds = 0
	for t in times:
		if not min or t < min:
			min = t
		if not max or t > max:
			max = t
		totalSeconds += t.hour*3600 + t.minute*60 + t.second
	avgSeconds = totalSeconds // len(times)
	h, leftover = divmod(avgSeconds, 3600)
	m, s = divmod(leftover, 60)
	avg = time(h, m, s)
	return (min, max, avg)



def calcHms (seconds):
	h, extra = divmod(seconds, 3600)
	m, s = divmod(extra, 60)
	return (h, m, s)


def ceilTime (t, delta):
	seconds = t.hour*3600 + t.minute*60 + t.second
	roundedSeconds = (seconds + delta.seconds) // delta.seconds * delta.seconds
	(h, m, s) = calcHms(roundedSeconds)
	roundedTime = time(h, m, s)
	return roundedTime
	

def download (url, folder, filename):
	downloadPath = os.path.join(folder, filename)
	with urllib.request.urlopen(url) as src, open(downloadPath, 'wb') as dst:
		shutil.copyfileobj(src, dst)
	return downloadPath


def floorTime (t, delta):
	seconds = t.hour*3600 + t.minute*60 + t.second
	roundedSeconds = seconds // delta.seconds * delta.seconds
	(h, m, s) = calcHms(roundedSeconds)
	roundedTime = time(h, m, s)
	return roundedTime
	

def getDeltas (dateTimes, descending=False):
	dtLast = None
	deltas = []
	for dtCurr in dateTimes:
		if dtLast:
			if descending:
				delta = dtLast-dtCurr
			else:
				delta = dtCurr-dtLast
			deltas.append(delta)
		dtLast = dtCurr
	return deltas


def modTo15Minutes (dt):
	tOrig = dt.time();
	h = 0
	m = tOrig.minute % 15
	s = tOrig.second
	t = time(h, m, s)
	return t


def modTo5Minutes (dt):
	tOrig = dt.time();
	h = 0
	m = tOrig.minute % 5
	s = tOrig.second
	t = time(h, m, s)
	return t

def modToHourly(dt):
	tOrig = dt.time();
	h = 0
	m = tOrig.minute
	s = tOrig.second
	t = time(h, m, s)
	return t


def printAlternating (lines, style1, style2):
	for i in range(0, len(lines)):
		if not i%2:
			s = style1 + lines[i]
		else:
			s = style2 + lines[i]
		print(s)


def printFancy (s, highlight=None, background=None):
	s = str(s)
	if (highlight): print(highlight*len(s))
	if (background): s = background + s + colorama.Fore.RESET + colorama.Back.RESET + colorama.Style.RESET_ALL
	print(s)
	if (highlight): print(highlight*len(s))


# Returns an open stream to the zipped file
# Assumes zipfile is a simple zipped file - there should be only one entry in this zip file.
# If not, throws an ex.
def unzip1 (sZipfile, folder=None):
	if not folder:
		folder = os.getcwd()
	with zipfile.ZipFile(sZipfile) as zip:
		infolist = zip.infolist()
		if len(infolist) != 1:
			raise Exception("{} contains more than one entry.".format(sZipfile))
		zi = infolist[0]
		data = zip.extract(zi, path=folder)
		path = os.path.join(folder, zi.filename)
	return path
		
