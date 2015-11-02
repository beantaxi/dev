import colorama
import datetime
import distutils.util
import http.cookiejar
import logging
import os.path
import shutil
import ssl
import sys
import urllib.request
import zipfile

def adjust (dt, weeks=0, days=0, hours=0, minutes=0, seconds=0, milliseconds=0, microseconds=0):
	localVars = dict(locals())
	del localVars['dt']
	td = datetime.timedelta(**localVars)
	dtNew = dt + td
	return dtNew


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
	sChoices = ' '.join(list(charChoices))
	if default:
		sChoices = sChoices.replace(default.lower(), default.upper())
	logging.debug("sChoices=" + sChoices)
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
	

def roundTime (t, delta=datetime.timedelta(minutes=1)):
	seconds = t.hour*3600 + t.minute*60 + t.second
	deltaSeconds = delta.seconds
	roundedSeconds = (seconds + deltaSeconds//2) // deltaSeconds * deltaSeconds
	h, extra = divmod(roundedSeconds, 3600)
	m, s = divmod(extra, 60)
	roundedTime = datetime.time(h, m, s)
	return roundedTime

def timeMinMaxAvg (datetimes):
	min = max = avg = None
	totalSeconds = 0
	for dt in datetimes:
		if not min or dt.time() < min:
			min = dt.time()
		if not max or dt.time() > max:
			max = dt.time()
		totalSeconds += dt.hour*3600 + dt.minute*60 + dt.second
	avgSeconds = totalSeconds // len(datetimes)
	h, leftover = divmod(avgSeconds, 3600)
	m, s = divmod(leftover, 60)
	logging.debug("h={} m={} s={}".format(str(h), str(m), str(s)))
	avg = datetime.time(h, m, s)
	return (min, max, avg)



def calcHms (seconds):
	h, extra = divmod(seconds, 3600)
	m, s = divmod(extra, 60)
	return (h, m, s)


def ceilTime (t, delta):
	seconds = t.hour*3600 + t.minute*60 + t.second
	roundedSeconds = (seconds + delta.seconds) // delta.seconds * delta.seconds
	(h, m, s) = calcHms(roundedSeconds)
	roundedTime = datetime.time(h, m, s)
	return roundedTime
	

def download (url, folder, filename):
	downloadPath = os.path.join(folder, filename)
	with urllib.request.urlopen(url) as src, open(downloadPath, 'wb') as dst:
		shutil.copyfileobj(src, dst)
	return downloadPath


def floorTime (t, delta):
	seconds = t.hour*3600 + t.minute*60 + t.second
	logging.debug("seconds=" + str(seconds))
	roundedSeconds = seconds // delta.seconds * delta.seconds
	(h, m, s) = calcHms(roundedSeconds)
	logging.debug("h={} m={} s={}".format(int(h), int(m), int(s)))
	roundedTime = datetime.time(h, m, s)
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


# Returns an open stream to the zipped file.
# Assumes zipfile is a simple zipped file - there should be only one entry in this zip file.
# If not, throws an ex.
def unzip (sZipfile):
	zip = zipfile.ZipFile(sZipfile)
	infolist = zip.infolist()
	if len(infolist) != 1:
		raise Exception("{} contains more than one entry.".format(sZipfile))
	ze = infolist[0]
	src = zip.open(ze)
	return src
