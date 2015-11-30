import urllib.parse
from ExtractTable import ExtractScheduleInfo

def addCronEntry (extractInfo, startTime, interval):
	extractId = extractInfo.id
	cmd = "{} {} {}".format(config.pythonPath, config.scriptPath, extractId)
	if interval == IntervalEnum.DAILY:
		cron = _utils.createDailyCron(startTime)
	else:
		cron = _utils.createFiveMinuteCron(startTime)
	logging.debug("cron=" + cron)
	_utils.printFancy("Appending this line to cron file", background=colorama.Back.GREEN)
	print()
	print(cron + ' ' + cmd)
	crontab = CronTab(user=True)
	job = crontab.new(command=cmd)
	job.setall(cron)
	job.enable()
	crontab.write()
	

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

