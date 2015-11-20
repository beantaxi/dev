#################################################################################
#
# parseReportList
#
description='Read a report listing & print out its information in a pleasant and useful manner'

# Get each tr, which has a td child with a csv report (we could have chosen xml instead - either/or)
xpathCsvFilenames = "//tr[td[@class='labelOptional_ind'][text()[contains(., '_csv')]]]/td[1]/text()"
xpathCsvUrl =      "(//tr[td[@class='labelOptional_ind'][text()[contains(., '_csv')]]])[1]/td[4]/div/a/@href"
xpathReports = '''
/html/body/form/table/tr[2]/td/table/tr[td[@class='labelOptional_ind'][text()[contains('.', '_csv')]]]
'''

import argparse
import datetime
import urllib.request
import ExtractTable
import X

def setupArgs (argParser):
	argParser.add_argument('whichReport')
	args = argParser.parse_args()
	return args

def getFilenames (htmlReportListing):
	filenames = htmlReportListing.xpath(xpathCsvFilenames)
	return filenames
	
if __name__ == '__main__':
	ap = argparse.ArgumentParser(description=description)
	args = setupArgs(ap)
	html = ExtractTable.getReport(args.whichReport)
	filenames = getFilenames(html)
	dtLast = None
	for filename in filenames:
		parts = filename.split('.')
		sDate = parts[3]
		sTime = parts[4]
		sDateTime = sDate + sTime
		sDateTimeFormat = '%Y%m%d%H%M%S%f'
		dt = datetime.datetime.strptime(sDateTime, sDateTimeFormat)
		if not dtLast:
			sDelta = "--"
		else:
			sDelta = str(dtLast - dt)
		print("{}, '{}', '{}'".format(sDateTime, dt, sDelta))
		dtLast = dt

