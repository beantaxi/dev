import argparse
import csv
import lxml.html
import os
import os.path
import shutil
import tempfile
import urllib.parse
import _utils
import Constants

class ExtractTable:
	def __init__ (self, tablePath, backupPath, tempTablePath):
		self.tablePath = tablePath
		self.backupPath = backupPath
		self.tempTablePath = tempTablePath

	def __getitem__ (self, i):
		data = self.all()
		extractInfo = data[i]
		return extractInfo

	def add (self, extractInfo):
		csvWriter = self._openCsvWriter()
		self._writeRow(csvWriter, extractInfo)

	def all (self):
		data = []
		csvReader = self._openCsvReader()
		for line in csvReader:
			extractInfo = ExtractInfo.fromLine(line)
			data.append(extractInfo)
		return data

	def backup (self):
		shutil.copy2(self.tablePath, self.backupPath)

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
		os.rename(self.tablePath, self.backupPath)
		
	def doesBackupExist (self):
		flag = os.path.exists(self.backupPath)
		return flag

	def getExtractInfo (self, arg):
		if arg.isdigit():
			n = arg
			if int(n)<10000:
				index = int(n)
				info = self.getExtractInfoByIndex(index)
			else:
				id = n
				info = self.getExtractInfoById(id)
		else:
			name = arg
			info = self.getExtractInfoByName(name)
		if not info:
			raise Exception("Extract info for {} not found in table".format(str(arg)))
		return info


	def getExtractInfoByIndex (self, index):
		data = self.all()
		info = data[index]
		return info 


	def getExtractInfoById (self, id):
		info = None
		data = self.all()
		for currInfo in data:
			if currInfo.id == id:
				info = currInfo
				break
		return info

	def getExtractInfoByName (self, name):
		info = None
		data = self.all()
		for currInfo in data:
			if currInfo.name == name:
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
		line = csvReader.read()
		extractInfo = ExtractInfo.fromLine(line)
		return extractInfo

	def _switchToTempTable (self):
		self._backupTable()
		# Rename temp file to current file
		os.rename(self.tempTablePath, self.tablePath)

	def _writeRow (self, csvWriter, extractInfo):
		csvWriter.writerow([extractInfo.id, extractInfo.name, extractInfo.url])

	def _writeRowToTempTable (self, extractInfo):
		csvWriter = self._openCsvWriter(self.tempTablePath)
		self._writeRow(csvWriter, extractInfo)

		

class ExtractInfo:
	
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


def addRow (table, id, name, url):
	extractInfo = ExtractInfo(id, name, url)
	table.add(extractInfo)


def backup (table):
	table.backup()
	print()
	print("Successfully backed up {} to {}".format(table.tablePath, table.backupPath))

def delete (table, iDelete):
	try:
		extractInfo = table[iDelete]
		s = "{0:<4}{1}".format(iDelete, extractInfo)
		_utils.printFancy(s, highlight='=')
		flag = _utils.askYesNoChoice("Delete row?", False)
		if flag:
			table.delete(iDelete)
			print("Row deleted.")
		else:
			print("Delete cancelled.")
	except Exception:
		print()
		print("Error deleting extract '{}' (extract might not exist)".format(iDelete))
	print()


# def downloadExtractList (table, arg):
# 	info = table.getExtractInfo(arg)
# 	filename = info.id + '.html'
# 	path = os.path.join(Constants.LISTINGS_FOLDER, filename)
# 	print("Downloading {} ...".format(info.url))
# 	with urllib.request.urlopen(info.url) as src, open(path, "wb") as dst:
# 		shutil.copyfileobj(src, dst)
# 	print("Downloaded {}.".format(filename))	

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


def getExtractId (arg):
	info = getInfo(arg)
	idExtract = info['id']
	return idExtract


def getExtract (table, arg):
	extractInfo = table.getExtractInfo(arg)
	url = extractInfo.url
	src = urllib.request.urlopen(url)
	html = lxml.html.parse(src)
	return html


def getExtractUrl (arg):
	info = getInfo(arg)
	url = info['url']
	return url


def getUrl (table, arg):
	extractInfo = table.getExtractInfo(arg)
	print(extractInfo.url)


def list (table):
	print()
	data = table.all()
	for i in range(0, len(data)):
		extractInfo = data[i]
		sInfo = str(extractInfo)
		sRow = "{0:<3}{1}".format(i, sInfo)
		print(sRow)
	print()

def listDetails (table):
	print()
	data = table.all()
	i = 0
	for extractInfo in data:
		sRow = "{0:<3}{1}".format(i, extractInfo)
		print(sRow)
		print(extractInfo.url)
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
	with open(Constants.TABLE_PATH) as extractTable:
		csvReader = csv.reader(extractTable)
		for row in csvReader:
			rows.append(row)
	return rows


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
	argParser.add_argument("--delete", nargs=1)
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
	table = ExtractTable(Constants.TABLE_PATH, Constants.BACKUP_TABLE_PATH, Constants.TEMP_TABLE_PATH)
	args = parseArgs()
	if args.addRow:
		id = args.addRow[0]
		name = args.addRow[1]
		url = args.addRow[2]
		addRow(table, id, name, url)
	elif args.backup:
		backup(table)
	elif args.delete:
		iDelete = int(args.delete[0])
		delete(table, iDelete)
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
