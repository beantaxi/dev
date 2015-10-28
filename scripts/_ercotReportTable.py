import X
import argparse
import csv
import lxml.html
import os
import os.path
import shutil
import tempfile
import urllib.parse
import _utils

class ErcotReportTable:

	def __getitem__ (self, i):
		data = self.all()
		reportInfo = data[i]
		return reportInfo

	def add (self, reportInfo):
		csvWriter = self._openCsvWriter()
		self._writeRow(csvWriter, reportInfo)

	def all (self):
		data = []
		csvReader = self._openCsvReader()
		for line in csvReader:
			reportInfo = ReportInfo.fromLine(line)
			data.append(reportInfo)
		return data

	def backup (self):
		shutil.copy2(X.TABLE_PATH, X.BACKUP_TABLE_PATH)

	def delete (self, iDelete):
		all = self.all()
		i = 0
		for info in all:
			if i != iDelete:
				self._writeRowToTempTable(info)
			i += 1
		self._switchToTempTable()

	def _backupTable (self):
		# Rename current file to bak
		os.rename(X.TABLE_PATH, X.BACKUP_TABLE_PATH)
		
	def doesBackupExist (self):
		flag = os.path.exists(X.BACKUP_TABLE_PATH)
		return flag

	def getReportInfo (self, arg):
		if arg.isdigit():
			n = arg
			if int(n)<10000:
				index = int(n)
				info = self.getReportInfoByIndex(index)
			else:
				id = n
				info = self.getReportInfoById(id)
		else:
			name = arg
			info = self.getReportInfoByName(name)
		if not info:
			raise Exception("Report info for {} not found in table".format(str(arg)))
		return info


	def getReportInfoByIndex (self, index):
		data = self.all()
		info = data[index]
		return info 


	def getReportInfoById (self, id):
		info = None
		data = self.all()
		for currInfo in data:
			if currInfo.id == id:
				info = currInfo
				break
		return info

	def getReportInfoByName (self, name):
		info = None
		data = self.all()
		for currInfo in data:
			if currInfo.name == name:
				info = currInfo
				break
		return info

	def restoreFromBackup (self):
		shutil.copy2(X.BACKUP_TABLE_PATH, X.TABLE_PATH)

	def _openCsvReader (self, filename=X.TABLE_PATH):
		f = open(filename, mode='r', newline='')
		csvReader = csv.reader(f, quoting=csv.QUOTE_NONNUMERIC)
		return csvReader

	def _openCsvWriter (self, filename=X.TABLE_PATH):
		f = open(filename, mode='a', newline='')
		csvWriter = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC)
		return csvWriter

	def _readRow (self, csvReader):
		line = csvReader.read()
		reportInfo = ReportInfo.fromLine(line)
		return reportInfo

	def _switchToTempTable (self):
		self._backupTable()
		# Rename temp file to current file
		os.rename(X.TEMP_TABLE_PATH, X.TABLE_PATH)

	def _writeRow (self, csvWriter, reportInfo):
		csvWriter.writerow([reportInfo.id, reportInfo.name, reportInfo.url])

	def _writeRowToTempTable (self, reportInfo):
		csvWriter = self._openCsvWriter(X.TEMP_TABLE_PATH)
		self._writeRow(csvWriter, reportInfo)

		

class ReportInfo:
	
	def __init__ (self, id, name, url):
		self.id = id
		self.name = name
		self.url = url

	@classmethod
	def fromLine (cls, line):
		id = line[0]
		name = line[1]
		url = line[2]
		info = cls(id, name, url)
		return info

	def __str__ (self):
		fmtInfo = "{0:<10}{1}"
		sInfo = fmtInfo.format(self.id, self.name)
		return sInfo


def addReportInfo (reportInfo):
	reportTable = ErcotReportTable()
	reportTable.add(reportInfo)


def addRow (id, name, url):
	reportInfo = ReportInfo(id, name, url)
	addReportInfo(reportInfo)


def printTable (path):
	with open(X.TABLE_PATH) as reportTable:
		csvReader = csv.reader(reportTable)
		for row in csvReader:
			print(row)


def parseArgs ():
	s = "Simple tool for managing the ERCOT report table"
	argParser = argparse.ArgumentParser()
	argParser.add_argument("--add-row", nargs=3, dest='addRow')
	argParser.add_argument("--backup", action='store_true')
	argParser.add_argument("--delete", nargs=1)
	argParser.add_argument("--download-report-list", nargs=1, dest='downloadReportList')
	argParser.add_argument("--get-url", nargs=1, dest='getUrl')
	argParser.add_argument("--list", action="store_true")
	argParser.add_argument("--list-details", action='store_true', dest='listDetails')
	argParser.add_argument("--manage", action="store_true")
	argParser.add_argument("--recover", action="store_true")
	argParser.add_argument("--test", action="store_true")
	args = argParser.parse_args()
	return args


def backup ():
	table = ErcotReportTable()
	table.backup()
	print()
	print("Successfully backed up {} to {}.".format(X.TABLE_PATH, X.BACKUP_TABLE_PATH))

def delete (iDelete):
	table = ErcotReportTable()
	try:
		reportInfo = table[iDelete]
		s = "{0:<4}{1}".format(iDelete, reportInfo)
		_utils.printFancy(s, highlight='=')
		flag = _utils.askYesNoChoice("Delete row?", False)
		if flag:
			table.delete(iDelete)
			print("Row deleted.")
		else:
			print("Delete cancelled.")
	except Exception:
		print()
		print("Error deleting report '{}' (report might not exist)".format(iDelete))
	print()


def downloadReportList (arg):
	table = ErcotReportTable()
	info = table.getReportInfo(arg)
	filename = info.id + '.html'
	path = os.path.join(X.LISTINGS_FOLDER, filename)
	print("Downloading {} ...".format(info.url))
	with urllib.request.urlopen(info.url) as src, open(path, "wb") as dst:
		shutil.copyfileobj(src, dst)
	print("Downloaded {}.".format(filename))	
	

def getInfoByIndex (index):
	rows = readTable()
	row = rows[index]
	info = rowToInfo(row)
	return info 


def getInfoById (id):
	info = None
	rows = readTable()
	for i in range(0, len(rows)):
		row = rows[i]
		currInfo = rowToInfo(row)
		if int(currInfo['id']) == id:
			info = currInfo
			break
	return info

def getInfoByName (name):
	info = None
	rows = readTable()
	found = False
	for i in range(0, len(rows)):
		row = rows[i]
		currInfo = rowToInfo(row)
		if currInfo['name'] == name:
			info = currInfo
			break
	return info


def getReportId (arg):
	info = getInfo(arg)
	idReport = info['id']
	return idReport


def getReport (arg):
	table = ErcotReportTable()
	reportInfo = table.getReportInfo(arg)
	url = reportInfo.url
	src = urllib.request.urlopen(url)
	html = lxml.html.parse(src)
	return html


def getReportUrl (arg):
	info = getInfo(arg)
	url = info['url']
	return url


def getUrl (arg):
	table = ErcotReportTable()
	reportInfo = table.getReportInfo(arg)
	print(reportInfo.url)


def list ():
	print()
	table = ErcotReportTable()
	data = table.all()
	for i in range(0, len(data)):
		reportInfo = data[i]
		sInfo = str(reportInfo)
		sRow = "{0:<3}{1}".format(i, sInfo)
		print(sRow)
	print()

def listDetails ():
	table = ErcotReportTable()
	print()
	data = table.all()
	i = 0
	for reportInfo in data:
		sRow = "{0:<3}{1}".format(i, reportInfo)
		print(sRow)
		print(reportInfo.url)
		i += 1
	print()
	

def manage ():
	pass


def printRow (i, highlight=None):
	rows = readTable()
	row = rows[i]
	info = rowToInfo(row)
	sInfo = infoToString(info)
	sRow = "{0:<3}{1}".format(i, sInfo)
	_utils.printFancy(sRow, highlight)


def readTable ():
	rows = []
	with open(X.TABLE_PATH) as reportTable:
		csvReader = csv.reader(reportTable)
		for row in csvReader:
			rows.append(row)
	return rows


def recover ():
	table = ErcotReportTable()
	print()
	if not table.doesBackupExist():
		print("No backup exists - recover aborted")
		print()
	else:
		choice = _utils.askYesNoChoice("Recover previous table file?", True)
		print()
		if choice:
			table.restoreFromBackup()
			print("Backup report file recovered.")
		else:
			print("Recovery cancelled.")
		print()


def test ():
	pass

if __name__ == "__main__":
	args = parseArgs()
	if args.addRow:
		id = args.addRow[0]
		name = args.addRow[1]
		url = args.addRow[2]
		addRow(id, name, url)
	elif args.backup:
		backup()
	elif args.delete:
		n = int(args.delete[0])
		delete(n)
	elif args.downloadReportList:
		arg = args.downloadReportList[0]
		downloadReportList(arg)
	elif args.getUrl:
		arg = args.getUrl[0]
		getUrl(arg)
	elif args.list:
		list()
	elif args.listDetails:
		listDetails()
	elif args.manage:
		manage()
	elif args.recover:
		recover()
	elif args.test:
		test()
	# printTable(X.TABLE_PATH)
