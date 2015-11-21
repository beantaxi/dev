import argparse
import logging
import os.path
import Constants
from ExtractTable import ExtractTable
import _utils

class ExtractStore:
	def __init__ (self, homeFolder):
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
	
	def download (self, extractInfo):
		url = extractInfo.url
		filename = extractInfo.id + '.html'
		folder = self.homeFolder
		listingPath = _utils.download(url, folder=folder, filename=filename)
		return listingPath

	def getAllListings (self):
		allFiles = os.listdir(self.homeFolder)
		allListings = [os.path.join(Constants.DOWNLOAD_FOLDER, f) for f in allFiles if ExtractStore.isListing(f)]
		return allListings

	def getLatestListing (self, id):
		pass

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
	ap.add_argument('--download', action='store_true')
	ap.add_argument('--exists', action='store_true')
	ap.add_argument('--list', action='store_true')
	ap.add_argument('--list-all', action='store_true', dest='listAll')
	args = ap.parse_args()
	return args


if __name__ == '__main__':
	store = ExtractStore(Constants.LISTINGS_FOLDER)
	table = ExtractTable()
	
	args = getArgs()
	arg = args.arg
	extractInfo = table.getExtractInfo(arg)
	
	if args.download:
		store.download(extractInfo)	
	elif args.exists:
		store.exists(extractInfo)
	elif args.list:
		pass
	elif args.listAll:
		pass
	else:
		logging.debug("extractInfo: {}".format(extractInfo))
