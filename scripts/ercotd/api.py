import colorama
from crontab import CronTab
from datetime import datetime
import urllib.parse
import config
import _utils
from FutureTechEx import FutureTechEx
from IntervalCalculator import IntervalEnum

class ExtractFilename:
	def __init__ (self, filename):
		self.filename = filename
		(reportId, dt) = parseExtractFilename(self.filename)
		self.reportId = reportId
		self.datetime = dt


def addCronEntry (info):
	cmd = "{} {} {}".format(config.pythonPath, config.scriptPath, info.reportId)
	if info.interval == IntervalEnum.DAILY:
		cron = _utils.createDailyCron(info.startTime)
	elif info.interval == IntervalEnum.FIFTEEN_MINUTES:
		cron = _utils.createMinuteCron(info.startTime, 15)
	elif info.interval == IntervalEnum.FIVE_MINUTES:
		cron = _utils.createMinuteCron(info.startTime, 5)
	elif info.interval == IntervalEnum.HOURLY:
		cron = _utils.createHourlyCron(info.startTime)
	else:
		raise Exception("Unknown interval! (" + str(info.interval) + ")")
	_utils.printFancy("Appending this line to cron file", background=colorama.Back.GREEN)
	print(cron + ' ' + cmd)
	crontab = CronTab(user=True)
	job = crontab.new(command=cmd, comment=info.reportName)
	job.setall(cron)
	job.enable()
	crontab.write()

def clearCronEntries ():
	crontab = CronTab(user=True)
	crontab.remove_all(config.scriptPath)
	crontab.write()


def downloadAndLog (url, folder, filename):
	path = _utils.download(url, folder, filename)
	_utils.unzip1(path, folderName)
	return path
	

# Sample filename:
# :
# cdr.00012300.0000000000000000.20151207.181016405.LMPSROSNODENP6788_20151207_181011_csv.zip
def parseExtractFilename (filename):
	parts = filename.split('.')
	reportId = parts[1].lstrip('0')
	sDate = parts[3]
	sTime = parts[4]
	sDateTime = sDate + sTime
	sDateTimeFormat = '%Y%m%d%H%M%S%f'
	dt = datetime.strptime(sDateTime, sDateTimeFormat)
	tuple = (reportId, dt)
	return tuple

def parseExtractListingUrl (url):
	validateExtractListingUrl(url)
	parts = urllib.parse.urlparse(url)
	q = urllib.parse.parse_qs(parts.query)
	id = q['reportTypeId'][0]
	name = q['reportTitle'][0]
	return (id, name)

def validateExtractListingUrl (url):
	parts = urllib.parse.urlparse(url)
	q = urllib.parse.parse_qs(parts.query)
	if not ('reportTypeId' in q.keys() and 'reportTitle' in q.keys()):
		raise Exception("This is not a valid extract listing url")

