import argparse
import logging
import os.path
import X
import _ercotReportTable
import _utils

class ReportListingStore:
	def __init__ (self, homeFolder):
		self.homeFolder = homeFolder

	@staticmethod
	def getReportId (filename):
		# id is the second part of the filename, and is eg '0000000012345'. So the
		# leading zeroes need to be trimmed. Thus, string->int->string.
		filenameParts = filename.split('.')
		idReport = str(int(filenameParts[1]))
		return idReport

	@staticmethod
	def isReportListing (filename):
		flag = filename.startswith('cdr') and filename.endswith('zip')
		return flag
	
	def download (self, reportInfo):
		url = reportInfo.url
		filename = reportInfo.id + '.html'
		folder = self.homeFolder
		listingPath = _utils.download(url, folder=folder, filename=filename)
		return listingPath

	def getAllListings (self):
		allFiles = os.listdir(self.homeFolder)
		allListings = [os.path.join(X.DOWNLOAD_FOLDER, f) for f in allFiles if ReportListingStore.isReportListing(f)]
		return allListings

	def getLatestListing (self, id):
		pass

	def getListings (self, id):
		allListings = self.getAllListings()
		listings = [f for f in allListings if getReportId(f) == id]
		return listings
	
	def hasListing (self, id):
		listings = self.getListings(id)
		flag = listings and len(listings) > 0
		return flag

def getArgs ():
	ap = argparse.ArgumentParser()
	ap.add_argument('arg')
	ap.add_argument('--download', action='store_true')
	ap.add_argument('--exists', action='store_true')
	ap.add_argument('--list', action='store_true')
	ap.add_argument('--list-all', action='store_true', dest='listAll')
	args = ap.parse_args()
	return args


def reportListingExists (idReport):
	listings = getReportListings(idReport)
	flag = bool(listings and len(listings))
	return flag


def getLatestReportListing (idReport):
	listings = getReportListings(idReport)
	sortedListings = sorted(listings, reverse=True, key=reportListingKey)
	latestListing = sortedListings[0]
	return latestListing


def getAllReportListings ():
	allFiles = os.listdir(X.DOWNLOAD_FOLDER)
	allListings = [os.path.join(X.DOWNLOAD_FOLDER, f) for f in allFiles if f.startswith('cdr') and f.endswith('zip')]
	return allListings

def getReportListings (idReport):
	allListings = getAllReportListings()
	reportListings = [f for f in allListings if str(int(f.split('.')[1])) == idReport]
	return reportListings
	

def reportListingKey (reportListingName):
	(pathname, filename) = os.path.split(reportListingName)
	parts = filename.split('.')
	key = parts[2] + parts[3]
	return key


def download (reportInfo):
	store = ReportListingStore(X.LISTINGS_FOLDER)
	listingPath = store.download(reportInfo)
	print("Downloaded {} to {}".format(reportInfo.url, listingPath))

def exists (reportInfo):
	store = ReportListingStore(X.LISTINGS_FOLDER)
	flag = store.hasListing(reportInfo.id)
	print("Listing for {} exists: {}".format(reportInfo.id, flag))

def list (reportInfo):
	pass

def listAll (reportInfo):
	pass

if __name__ == '__main__':
	listingsStore = ReportListingStore(X.LISTINGS_FOLDER)
	reportTable = _ercotReportTable.ErcotReportTable()
	
	args = getArgs()
	arg = args.arg
	reportInfo = reportTable.getReportInfo(arg)
	
	if args.download:
		download(reportInfo)	
	elif args.exists:
		exists(reportInfo)
	elif args.list:
		list(reportInfo)	
	elif args.listAll:
		listAll(reportInfo)
	else:
		logging.debug("reportInfo: {}".format(reportInfo))
#	logging.debug("idReport={}".format(idReport))
#	if reportListingExists(idReport):
#		filename = getLatestReportListing(idReport)
#		with _utils.unzip(filename) as src:
#			for line in src:
#				print(line)

	
