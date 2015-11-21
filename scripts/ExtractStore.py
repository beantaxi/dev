import argparse
import logging
import os.path
import Constants
from ExtractTable import ExtractTable
from ExtractListing import ExtractListing
import _utils

class ExtractStore:
	def __init__ (self, extractTable, homeFolder):
		self.extractTable = extractTable
		self.homeFolder = homeFolder

	@staticmethod
	def getExtractId (filename):
		# id is the second part of the filename, and is eg '0000000012345'. So the
		# leading zeroes need to be trimmed. Thus, string->int->string.
		filenameParts = filename.split('.')
		idExtract = str(int(filenameParts[1]))
		return idExtract

	@staticmethod
	def isListing (filename):
		flag = filename.startswith('cdr') and filename.endswith('zip')
		return flag
	
	def downloadLatestExtract (self, extractId):
		listing = self.downloadListing(extractId)
		latestExtractInfo = listing.extractInfo[next(iter(listing.extractInfo))]
		url = latestExtractInfo['url']
		filename = latestExtractInfo['filename']
		path = _utils.download(url, self.homeFolder, filename)
		_utils.unzip(path, self.homeFolder)
		return path

	def downloadListing (self, extractId):
		extractInfo = 	self.extractTable.getExtractInfo(extractId)
		url = extractInfo.url
		filename = extractInfo.id + '.html'
		folder = os.path.join(self.homeFolder, 'listings')
		listingPath = _utils.download(url, folder=folder, filename=filename)
		listing = ExtractListing(listingPath)
		return listing

	def getAllListings (self):
		allFiles = os.listdir(self.homeFolder)
		allListings = [os.path.join(Constants.DOWNLOAD_FOLDER, f) for f in allFiles if ExtractStore.isListing(f)]
		return allListings

	def getLatestExtract (self, id):
		pass
		# Download listing for this
		# Get the url and file name for the topmost report
		# Download and save the file
		# Open the downloaded file and return it

	def getListings (self, id):
		allListings = self.getAllListings()
		listings = [f for f in allListings if getExtractId(f) == id]
		return listings
	
	def hasListing (self, id):
		listings = self.getListings(id)
		flag = listings and len(listings) > 0
		return flag

def getArgs ():
	ap = argparse.ArgumentParser()
	ap.add_argument('arg')
	ap.add_argument('-de', '--downloadExtract', action='store_true')
	ap.add_argument('-dl', '--downloadListing', action='store_true')
	ap.add_argument('--exists', action='store_true')
	ap.add_argument('--list', action='store_true')
	ap.add_argument('--list-all', action='store_true', dest='listAll')
	args = ap.parse_args()
	return args

if __name__ == '__main__':
	table = ExtractTable(Constants.TABLE_PATH, Constants.BACKUP_TABLE_PATH, Constants.TEMP_TABLE_PATH)
	store = ExtractStore(table, Constants.LISTINGS_FOLDER)
	args = getArgs()
	arg = args.arg
	
	if args.downloadExtract:
		path = store.downloadLatestExtract(arg)
		print(path)
	elif args.downloadListing:
		listing = store.downloadListing(arg)
		firstKey = next(iter(listing.extractInfo))
		print(listing.extractInfo[firstKey])
	elif args.exists:
		store.exists(extractInfo)
	elif args.list:
		pass
	elif args.listAll:
		pass
	elif args.exists:
		store.exists(extractInfo)
	elif args.list:
		pass
	elif args.listAll:
		pass
	else:
		logging.debug("extractInfo: {}".format(extractInfo))
