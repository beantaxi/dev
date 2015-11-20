import argparse
import logging
import os.path
import X
import ExtractTable
import _utils

def getArgs ():
	ap = argparse.ArgumentParser()
	ap.add_argument('arg')
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


if __name__ == '__main__':
	args = getArgs()
	arg = args.arg
	idReport = ExtractTable.getReportId(arg)
	logging.debug("idReport={}".format(idReport))
	if reportListingExists(idReport):
		filename = getLatestReportListing(idReport)
		with _utils.unzip(filename) as src:
			for line in src:
				print(line)

	
