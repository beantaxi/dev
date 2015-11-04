###############################################################################
#
# addErcotReportToTable.py
#
# Process a report listing URL, and add it to the report table.
#
# The URL is parsed for the report id and name. The user is then
# presented these values, and given a chance to take them as-is,
# or to alter them. (This is primarily intended to allow for a name
# change on very long report names - I'm not sure there is actually
# a reason to support changing the id but it's there anyway.)
#
# Once the user is happy with the changes, they will get appended
# to the end of the report table, defined by TABLE_PATH.
#

import sys
import X
import abc
import argparse
import colorama
import crontab
import datetime
import distutils.util
import lxml.html
import logging
import time
import urllib.parse
import urllib.request
import _ercotReportTable
import _getReportUrlInfo
import _utils
from FutureTechEx import FutureTechEx
from IntervalCalculator import IntervalCalculator
from IntervalCalculator import IntervalEnum
from TimeDelta2 import TimeDelta2
from ReportListing import ReportListing

class Stage (abc.ABC):
	@abc.abstractmethod
	def execute (self, data):
		pass


class GetReportInfo (Stage):
	def execute (self, data):
		reportInfo = data['defaultReportInfo']
		done = False
		while not done:
			print()
			print(colorama.Back.BLUE + 'Report Info' + colorama.Fore.RESET + colorama.Back.RESET + colorama.Style.RESET_ALL)
			printReportInfo(reportInfo)
			prompt = "Are these values OK?"
			isOk = _utils.askYesNoChoice(prompt, 'Y')
			if isOk:
				done = True
			else:
				print("No problem - let's make some changes")
				fmtPrompt = "{} [{}]: "
				prompt = fmtPrompt.format("New id", reportInfo.id)
				newId = input(prompt)
				if newId == "":
					newId = reportInfo.id
				prompt = fmtPrompt.format("New name", reportInfo.name)
				newName = input(prompt)
				if newName == "":
					newName = reportInfo.name
				print("Your new id is {} and your new name is '{}'".format(newId, newName))
				reportInfo.id = newId
				reportInfo.name = newName
		data['reportInfo'] = reportInfo
		return data

class GetSchedule (Stage):
	@classmethod
	def askForInterval ():
		prompt = "Choose Daily, Hourly, or Five Minute interval (D, H, 5): "
		interval = input(prompt)	
		

	@classmethod
	def getStartTime (cls, datetimes, interval):
		print("It looks like the report has the following times")
		if interval == IntervalEnum.DAILY:
			times = [dt.time() for dt in datetimes]
			(tMin, tMax, tAvg) = _utils.timeMinMaxAvg(times)
			rounding = datetime.timedelta(minutes=5)
			roundedMin = _utils.floorTime(tMin, rounding)
			roundedMax = _utils.ceilTime(tMax, rounding)
			roundedAvg = _utils.roundTime(tAvg, rounding)
			printTimeLine("Min", tMin, roundedMin)
			printTimeLine("Max", tMax, roundedMax)
			printTimeLine("Avg", tAvg, roundedAvg)
			print()
			promptFmt = "Would you like to choose the rounded Mi{0}n{1}, Ma{0}x{1}, {0}A{1}vg, or {0}O{1}ther?"
			prompt = promptFmt.format(colorama.Fore.BLUE + colorama.Style.BRIGHT, colorama.Style.RESET_ALL)
			choices = "nxao"
			choiceMap = {'n': roundedMin, 'x': roundedMax, 'a': roundedAvg}
			choice = _utils.askMultiChoice(prompt, choices)
			logging.debug("choice=" + choice)
			if choice in choiceMap:
				startTime = choiceMap[choice]
			else:
				startTime = _utils.askTime("What time would you like? [HH:MM] ", "%H:%M")
		elif interval == IntervalEnum.FIVE_MINUTES:
			times = [_utils.modTo5Minutes(dt) for dt in datetimes]
			(tMin, tMax, tAvg) = _utils.timeMinMaxAvg(times)
			rounding = datetime.timedelta(seconds=1)
			roundedMin = _utils.floorTime(tMin, rounding)
			roundedMax = _utils.ceilTime(tMax, rounding)
			roundedAvg = _utils.roundTime(tAvg, rounding)
			printTimeLine("Min", tMin, roundedMin)
			printTimeLine("Max", tMax, roundedMax)
			printTimeLine("Avg", tAvg, roundedAvg)
			print()
			promptFmt = "Would you like to choose the rounded Mi{0}n{1}, Ma{0}x{1}, {0}A{1}vg, or {0}O{1}ther?"
			prompt = promptFmt.format(colorama.Fore.BLUE + colorama.Style.BRIGHT, colorama.Style.RESET_ALL)
			choices = "nxao"
			choiceMap = {'n': roundedMin, 'x': roundedMax, 'a': roundedAvg}
			choice = _utils.askMultiChoice(prompt, choices)
			logging.debug("choice=" + choice)
			if choice in choiceMap:
				startTime = choiceMap[choice]
			else:
				startTime = _utils.askTime("What time would you like? [MM:SS] ", "%M:%S")
			logging.debug("startTime=" + str(startTime))

			# Create a strip of the times, modding the minutes by 5
			# Check out time min max rounding on that. Maybe the method should know how.
			# The rest I guess will fall out of that.
		else:
			raise FutureTechEx("No support for interval=" + str(interval))
		return startTime


	def execute (self, data):
		print()
		_utils.printFancy("Get Schedule", background=colorama.Back.BLUE)
		reportInfo = data['reportInfo']
		with urllib.request.urlopen(reportInfo.url) as src:
			html = lxml.html.parse(src)
		listing = ReportListing(html)
		reportDateTimes = listing.getDateTimes()
		n = min(len(reportDateTimes), 10)
		dtLast = None
		deltas = []
		for i in range(0, n):
			dtCurr = reportDateTimes[i]
			sDt = str(dtCurr)
			if not dtLast:
				sDelta = "--"
			else:
				delta = dtLast-dtCurr
				sDelta = TimeDelta2.toString(delta)
				deltas.append(delta)
			print("{:32}{}".format(sDt, sDelta))
			time.sleep(0.1)
			dtLast = dtCurr
		interval = IntervalCalculator.getInterval(deltas)
		print()
		print("The interval for these reports appears to be {}{}".format(colorama.Fore.CYAN, interval))
		print()
		choice = _utils.askYesNoChoice("Is this correct?", default=True)
		if choice:
			print()
			_utils.printFancy("Saving the interval as {}".format(interval), background=colorama.Back.GREEN)
			print()
		else:
			interval = askForInterval()
		data['interval'] = interval

		startTime = self.__class__.getStartTime(reportDateTimes, interval)
		data['startTime'] = startTime


def printTimeLine (label, t, roundedTime):
	timeFormat = "%H:%M:%S"
	sTime = t.strftime(timeFormat)
	sRoundedTime = roundedTime.strftime(timeFormat)
	line = "{:5}{:18}{:18}".format(label, sTime, sRoundedTime)
	print(line)
	
def printReportInfo (reportInfo):
	fmt = "{:<6} {}"
	print(fmt.format("id", reportInfo.id))
	print(fmt.format("name", reportInfo.name))
	print()
	

def askForReportInfo (reportInfo):
	done = False
	while not done:
		print()
		print(colorama.Back.BLUE + 'Report Info' + colorama.Fore.RESET + colorama.Back.RESET + colorama.Style.RESET_ALL)
		printReportInfo(reportInfo)
		prompt = "Are these values OK?"
		isOk = _utils.askYesNoChoice(prompt, 'Y')
		if isOk:
			done = True
		else:
			print("No problem - let's make some changes")
			fmtPrompt = "{} [{}]: "
			prompt = fmtPrompt.format("New id", reportInfo.id)
			newId = input(prompt)
			if newId == "":
				newId = reportInfo.id
			prompt = fmtPrompt.format("New name", reportInfo.name)
			newName = input(prompt)
			if newName == "":
				newName = reportInfo.name
			print("Your new id is {} and your new name is '{}'".format(newId, newName))
			reportInfo.id = newId
			reportInfo.name = newName
	return reportInfo
	
if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Parse a report URL and add it to the report table.")

	parser.add_argument("url", help="ERCOT report url to parse")
	args = parser.parse_args()
	url = args.url
	logging.debug("url=" + url)
	
	if not vars(args) or len(args.url) == 0:
		parser.print_help()
		sys.exit(0)

	# Add basic report data to table
	defaultReportInfo = _getReportUrlInfo.parse(args.url)
	data = {'defaultReportInfo': defaultReportInfo}
	stage = GetReportInfo()
	stage.execute(data)
	reportInfo = data['reportInfo']
	_ercotReportTable.addReportInfo(reportInfo)
	msg = "'{}' (id={}) has been added to the report table.".format(reportInfo.name, reportInfo.id)
	print()
	print(colorama.Back.GREEN + msg)

	# Try and figure out schedule
	stage = GetSchedule()
	stage.execute(data)
	interval = data['interval']
	startTime = data['startTime']
	print("OK, we'll go with a starttime of " + str(startTime))
	pythonPath = "/home/ubuntu/dev/py/venv/main/bin/python3" 
	pythonScript = "/home/ubuntu/work/euclid/scripts/getReportListing.py"
	reportId = reportInfo.id
	cmd = "{} {} {}".format(pythonPath, pythonScript, reportId)
	if interval == IntervalEnum.DAILY:
		cron = _utils.createDailyCron(startTime)
	else:
		cron = _utils.createFiveMinuteCron(startTime)
	logging.debug("cron=" + cron)
	_utils.printFancy("Appending this line to cron file", background=colorama.Back.GREEN)
	print()
	print(cron + ' ' + cmd)
	crontab = crontab.CronTab(user=True)
	job = crontab.new(command=cmd)
	job.setall(cron)
	job.enable()
	crontab.write()

# Prompt if they are ok

# If no
	# Get new id, defaulting to current id
	# Get new name, defaulting to current name
# Print line - later we'll append this to the main file, possibly using a CSV API


#
#url = urllib.parse.urlparse(sUrl)
#resp = urllib.request.urlopen(sUrl)
#html = resp.read()
#print(html)

