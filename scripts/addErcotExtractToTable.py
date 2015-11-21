###############################################################################
#
# addExtractToTable.py
#
# Process a extract listing URL, and add it to the extract table.
#
# The URL is parsed for the extract id and name. The user is then
# presented these values, and given a chance to take them as-is,
# or to alter them. (This is primarily intended to allow for a name
# change on very long extract names - I'm not sure there is actually
# a reason to support changing the id but it's there anyway.)
#
# Once the user is happy with the changes, they will get appended
# to the end of the extract table, defined by TABLE_PATH.
#

import sys
import X
import abc
import argparse
import colorama
import config
from crontab import CronTab
import datetime
import distutils.util
import lxml.html
import logging
import time
import urllib.parse
import urllib.request
import ExtractTable
import _getExtractUrlInfo
import _utils
from FutureTechEx import FutureTechEx
from IntervalCalculator import IntervalCalculator
from IntervalCalculator import IntervalEnum
from TimeDelta2 import TimeDelta2
from ExtractListing import ExtractListing

class Stage (abc.ABC):
	@abc.abstractmethod
	def execute (self, data):
		pass


class GetExtractInfo (Stage):
	def execute (self, data):
		extractInfo = data['defaultExtractInfo']
		done = False
		while not done:
			print()
			print(colorama.Back.BLUE + 'Extract Info' + colorama.Fore.RESET + colorama.Back.RESET + colorama.Style.RESET_ALL)
			printExtractInfo(extractInfo)
			prompt = "Are these values OK?"
			isOk = _utils.askYesNoChoice(prompt, 'Y')
			if isOk:
				done = True
			else:
				print("No problem - let's make some changes")
				fmtPrompt = "{} [{}]: "
				prompt = fmtPrompt.format("New id", extractInfo.id)
				newId = input(prompt)
				if newId == "":
					newId = extractInfo.id
				prompt = fmtPrompt.format("New name", extractInfo.name)
				newName = input(prompt)
				if newName == "":
					newName = extractInfo.name
				print("Your new id is {} and your new name is '{}'".format(newId, newName))
				extractInfo.id = newId
				extractInfo.name = newName
		data['extractInfo'] = extractInfo
		return data


class GetSchedule (Stage):
	@classmethod
	def askForInterval ():
		prompt = "Choose Daily, Hourly, or Five Minute interval (D, H, 5): "
		interval = input(prompt)	

	@classmethod
	def getStartTime (cls, datetimes, interval):
		print("It looks like the extract has the following times")
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
		extractInfo = data['extractInfo']
		with urllib.request.urlopen(extractInfo.url) as src:
			html = lxml.html.parse(src)
		listing = ExtractListing(html)
		extractDateTimes = listing.getDateTimes()
		n = min(len(extractDateTimes), 10)
		dtLast = None
		deltas = []
		for i in range(0, n):
			dtCurr = extractDateTimes[i]
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
		print("The interval for these extracts appears to be {}{}".format(colorama.Fore.CYAN, interval))
		print()
		choice = _utils.askYesNoChoice("Is this correct?", default=True)
		if choice:
			print()
			_utils.printFancy("Saving the interval as {}".format(interval), background=colorama.Back.GREEN)
			print()
		else:
			interval = askForInterval()
		data['interval'] = interval

		startTime = self.__class__.getStartTime(extractDateTimes, interval)
		data['startTime'] = startTime


def printTimeLine (label, t, roundedTime):
	timeFormat = "%H:%M:%S"
	sTime = t.strftime(timeFormat)
	sRoundedTime = roundedTime.strftime(timeFormat)
	line = "{:5}{:18}{:18}".format(label, sTime, sRoundedTime)
	print(line)
	
def printExtractInfo (extractInfo):
	fmt = "{:<6} {}"
	print(fmt.format("id", extractInfo.id))
	print(fmt.format("name", extractInfo.name))
	print()
	

def askForExtractInfo (extractInfo):
	done = False
	while not done:
		print()
		print(colorama.Back.BLUE + 'Extract Info' + colorama.Fore.RESET + colorama.Back.RESET + colorama.Style.RESET_ALL)
		printExtractInfo(extractInfo)
		prompt = "Are these values OK?"
		isOk = _utils.askYesNoChoice(prompt, 'Y')
		if isOk:
			done = True
		else:
			print("No problem - let's make some changes")
			fmtPrompt = "{} [{}]: "
			prompt = fmtPrompt.format("New id", extractInfo.id)
			newId = input(prompt)
			if newId == "":
				newId = extractInfo.id
			prompt = fmtPrompt.format("New name", extractInfo.name)
			newName = input(prompt)
			if newName == "":
				newName = extractInfo.name
			print("Your new id is {} and your new name is '{}'".format(newId, newName))
			extractInfo.id = newId
			extractInfo.name = newName
	return extractInfo


def addCronEntry (startTime, interval):
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
	

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Parse a extract URL and add it to the extract table.")

	parser.add_argument("url", help="ERCOT extract url to parse")
	args = parser.parse_args()
	url = args.url
	logging.debug("url=" + url)
	
	if not vars(args) or len(args.url) == 0:
		parser.print_help()
		sys.exit(0)

	# Add basic extract data to table
	defaultExtractInfo = _getExtractUrlInfo.parse(args.url)
	data = {'defaultExtractInfo': defaultExtractInfo}
	stage = GetExtractInfo()
	stage.execute(data)
	extractInfo = data['extractInfo']
	ExtractTable.addExtractInfo(extractInfo)
	msg = "'{}' (id={}) has been added to the extract table.".format(extractInfo.name, extractInfo.id)
	print()
	print(colorama.Back.GREEN + msg)

	# Try and figure out schedule
	stage = GetSchedule()
	stage.execute(data)
	interval = data['interval']
	startTime = data['startTime']
	addCronEntry(startTime, interval)

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

