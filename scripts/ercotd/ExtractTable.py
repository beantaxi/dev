import argparse
import csv
import datetime
import lxml.html
import os
import os.path
import shutil
from signal import signal, SIGPIPE, SIG_DFL # (thank you SO)
import tempfile
import urllib.parse
import api
import _utils
import Constants
from IntervalCalculator import IntervalEnum

#class ExtractInfo:
#	def __init__ (self, id, name, url):
#		self.id = id
#		self.name = name
#		self.url = url
#
#	@classmethod
#	def fromRow (cls, line):
#		id = line[0]
#		name = line[1]
#		url = line[2]
#		info = cls(id, name, url)
#		return info
#
#	def __str__ (self):
#		fmtInfo = "{0:<10}{1}"
#		sInfo = fmtInfo.format(self.id, self.name)
#		return sInfo


class ExtractScheduleInfo:
	def __init__ (self, reportId, reportName, url, interval, startTime):

		self.url = url
		self.reportId = reportId
		self.reportName = reportName
		self.interval = interval
		self.startTime = startTime
	
	@classmethod
	def fromRow (cls, row):
		id = row[0]
		name = row[1]
		url = row[2]
		interval = IntervalEnum.fromstring(row[3])
		startTime = datetime.datetime.strptime(row[4], "%H:%M")
		info = cls(id, name, url, interval, startTime)
		return info

	def pretty (self):
		sInterval = self.interval.tostring()
		sStartTime = self.startTime.strftime("%H:%M")
		fmt = "{0:<8}{1:<60}{2:<16}{3:<5}"
		s = fmt.format(self.reportId, self.reportName, sInterval, sStartTime)
		return s

	def toRow (self):
		sInterval = self.interval.tostring()
		sStartTime = self.startTime.strftime("%H:%M")
		row = [self.reportId, self.reportName, self.url, sInterval, sStartTime]
		return row

class ExtractTable:
	def __init__ (self, tablePath, backupPath, tempTablePath):
		self.tablePath = tablePath
		self.backupPath = backupPath
		self.tempTablePath = tempTablePath

	def __getitem__ (self, reportId):
		data = self.all()
		for currInfo in data:
			if currInfo.reportId == reportId:
				info = currInfo
				break
		return info

	def add (self, info):
		csvWriter = self._openCsvWriter()
		self._writeRow(csvWriter, info)

	def all (self):
		data = []
		csvReader = self._openCsvReader()
		for row in csvReader:
			info = ExtractScheduleInfo.fromRow(row)
			data.append(info)
		return data

	def backup (self):
		shutil.copy2(self.tablePath, self.backupPath)

	def delete (self, reportId):
		open(self.tempTablePath, "w").close()
		for info in self.all():
			if reportId != info.reportId:
				self._writeRowToTempTable(info)
		self._switchToTempTable()

	def _backupTable (self):
		# Rename current file to bak
		os.rename(self.tablePath, self.backupPath)
		
	def doesBackupExist (self):
		flag = os.path.exists(self.backupPath)
		return flag

	def getInfo (self, arg):
		if arg.isdigit():
			n = arg
			if int(n)<10000:
				index = int(n)
				info = self.getInfoByIndex(index)
			else:
				id = n
				info = self.getInfoById(id)
		else:
			name = arg
			info = self.getInfoByName(name)
		if not info:
			raise Exception("Schedule info for {} not found in table".format(str(arg)))
		return info


	def getInfoByIndex (self, index):
		data = self.all()
		info = data[index]
		return info 


	def getInfoById (self, reportId):
		info = None
		data = self.all()
		for currInfo in data:
			if currInfo.reportId == reportId:
				info = currInfo
				break
		return info

	def getInfoByName (self, reportName):
		info = None
		data = self.all()
		for currInfo in data:
			if currInfo.reportName == reportName:
				info = currInfo
				break
		return info

	def restoreFromBackup (self):
		shutil.copy2(self.backupPath, self.tablePath)

	def _openCsvReader (self, filename=None):
		if filename == None:
			filename = self.tablePath
		f = open(filename, mode='r', newline='')
		csvReader = csv.reader(f, quoting=csv.QUOTE_NONNUMERIC)
		return csvReader

	def _openCsvWriter (self, filename=None):
		if filename == None:
			filename = self.tablePath
		f = open(filename, mode='a', newline='')
		csvWriter = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC)
		return csvWriter

	def _readRow (self, csvReader):
		row = csvReader.read()
		scheduleInfo = ExtractScheduleInfo.fromRow(row)
		return scheduleInfo

	def _switchToTempTable (self):
		self._backupTable()
		# Rename temp file to current file
		os.rename(self.tempTablePath, self.tablePath)

	def _writeRow (self, csvWriter, info):
		row = info.toRow()
		csvWriter.writerow(row)

	def _writeRowToTempTable (self, info):
		csvWriter = self._openCsvWriter(self.tempTablePath)
		self._writeRow(csvWriter, info)

		
def addRow (table, url, interval, startTime):
	(reportId, reportName) = api.parseExtractListingUrl(url)
	info = ExtractScheduleInfo(reportId, reportName, url, interval, startTime)
	table.add(info)


def backup (table):
	table.backup()
	print()
	print("Successfully backed up {} to {}".format(table.tablePath, table.backupPath))
#
def delete (table, reportId):
	try:
		info = table[reportId]
		s = info.pretty()
		_utils.printFancy(s, highlight='=')
		flag = _utils.askYesNoChoice("Delete row?", False)
		if flag:
			table.delete(reportId)
			print("Row deleted.")
		else:
			print("Delete cancelled.")
	except Exception:
		print()
		print("Error deleting extract '{}' (extract might not exist)".format(reportId))
	print()


def generateCron (table):
	api.clearCronEntries()
	data = table.all()
	for info in data:
		api.addCronEntry(info)


# def downloadExtractList (table, arg):
# 	info = table.getExtractInfo(arg)
# 	filename = info.id + '.html'
# 	path = os.path.join(Constants.LISTINGS_FOLDER, filename)
# 	print("Downloading {} ...".format(info.url))
# 	with urllib.request.urlopen(info.url) as src, open(path, "wb") as dst:
# 		shutil.copyfileobj(src, dst)
# 	print("Downloaded {}.".format(filename))	

#def getInfoByIndex (index):
#	rows = readTable()
#	row = rows[index]
#	info = rowToInfo(row)
#	return info 
#
#
#def getInfoById (id):
#	info = None
#	rows = readTable()
#	for i in range(0, len(rows)):
#		row = rows[i]
#		currInfo = rowToInfo(row)
#		if int(currInfo['id']) == id:
#			info = currInfo
#			break
#	return info
#
#def getInfoByName (name):
#	info = None
#	rows = readTable()
#	found = False
#	for i in range(0, len(rows)):
#		row = rows[i]
#		currInfo = rowToInfo(row)
#		if currInfo['name'] == name:
#			info = currInfo
#			break
#	return info
#
#
#def getExtractId (arg):
#	info = getInfo(arg)
#	idExtract = info['id']
#	return idExtract
#
#
#def getExtract (table, arg):
#	extractInfo = table.getExtractInfo(arg)
#	url = extractInfo.url
#	src = urllib.request.urlopen(url)
#	html = lxml.html.parse(src)
#	return html
#
#
#def getExtractUrl (arg):
#	info = getInfo(arg)
#	url = info['url']
#	return url
#
#
def getUrl (table, arg):
	info = table.getInfo(arg)
	print(info.url)


def list (table):
	data = table.all()
	for i, info in enumerate(data):
		sInfo = info.pretty()
		s = "{0:<3}{1}".format(i, sInfo)
		print(s)

def listDetails (table):
	print()
	data = table.all()
	for i, info in enumerate(data):
		sInfo = info.pretty()
		s = "{0:<3}{1}".format(i, sInfo)
		print(s)
		print(info.url)
	print()
	

def manage ():
	pass


def recover (table):
	print()
	if not table.doesBackupExist():
		print("No backup exists - recover aborted")
		print()
	else:
		choice = _utils.askYesNoChoice("Recover previous table file?", True)
		print()
		if choice:
			table.restoreFromBackup()
			print("Backup extract file recovered.")
		else:
			print("Recovery cancelled.")
		print()


def test ():
	pass

def parseArgs ():
	s = "Simple tool for managing the ERCOT extract table"
	argParser = argparse.ArgumentParser()
	argParser.add_argument("--add-row", nargs=3, dest='addRow')
	argParser.add_argument("--backup", action='store_true')
	argParser.add_argument("-cron", "--generate-cron", action="store_true", dest='generateCron')
	argParser.add_argument("-d", "--delete", nargs=1)
	argParser.add_argument("-dl", "--download", nargs=1)
	argParser.add_argument("--download-extract-list", nargs=1, dest='downloadExtractList')
	argParser.add_argument("--get-url", nargs=1, dest='getUrl')
	argParser.add_argument("--list", action="store_true")
	argParser.add_argument("--list-details", action='store_true', dest='listDetails')
	argParser.add_argument("--manage", action="store_true")
	argParser.add_argument("--recover", action="store_true")
	argParser.add_argument("--test", action="store_true")
	args = argParser.parse_args()
	return args


if __name__ == "__main__":
	signal(SIGPIPE, SIG_DFL)
	table = ExtractTable(Constants.TABLE_PATH, Constants.BACKUP_TABLE_PATH, Constants.TEMP_TABLE_PATH)
	args = parseArgs()
	if args.addRow:
		url = args.addRow[0]
		interval = IntervalEnum.fromstring(args.addRow[1])
		startTime = datetime.datetime.strptime(args.addRow[2], "%H:%M")
		addRow(table, url, interval, startTime)
	elif args.backup:
		backup(table)
	elif args.delete:
		reportId = args.delete[0]
		delete(table, reportId)
	elif args.download:
		reportId = args.download[0]
		download(table, reportId)
	elif args.generateCron:
		generateCron(table)
	elif args.getUrl:
		arg = args.getUrl[0]
		getUrl(table, arg)
	elif args.list:
		list(table)
	elif args.listDetails:
		listDetails(table)
	elif args.manage:
		manage(table)
	elif args.recover:
		recover(table)
	elif args.test:
		test()
