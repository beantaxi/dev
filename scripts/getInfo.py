###############################################################################
#
# getInfo.py
#
# Process a python report URL, and add it to the report table.
#
# The URL is parsed for the report id and name. The user is then
# presented these values, and given a chance to take them as-is,
# or to alter them. (This is primarily intended to allow for a name
# change on very long report names - I'm not sure there is actually
# a reason to support changing the id but it's there anyway.
#
# Once the user is happy with the changes, they will get appended
# to the end of the report table, defined by TABLE_PATH.
#

TABLE_PATH = "/home/chrissy/work/euclid/scripts/ercotReportTable.txt"

import argparse
import sys
import distutils.util
import urllib.parse
import urllib.request
import _getReportUrlInfo

def printInfo (info):
	fmt = "{:<6} {}"
	print()
	print(fmt.format("id", info['id']))
	print(fmt.format("name", info['name']))
	print()
	

def getYesNoChoice (prompt, default=None):
	if default == None:	
		prompt = prompt + (" (y/n) ")
	else:
		sDefault = str(default)
		default = distutils.util.strtobool(sDefault)
		if default == True:
			prompt = prompt + (" (Y/n) ")
		else:
			prompt = prompt + (" (y/N) ")
	choice = None
	while choice == None:
		try:
			sChoice = input(prompt)
			if sChoice == "" and default is not None:
				sChoice = str(default)
			choice = distutils.util.strtobool(sChoice)
		except ValueError:
			print("Invalid choice: " + sChoice)
	return choice	
	


def askForNewInfo (info):
	done = False
	while not done:
		prompt = "Are these values OK?"
		isOk = getYesNoChoice(prompt, 'Y')
		if isOk:
			done = True
		else:
			print("No problem - let's make some changes")
			fmtPrompt = "{} [{}]: "
			prompt = fmtPrompt.format("New id", info['id'])
			newId = input(prompt)
			if newId == "":
				newId = info['id']
			prompt = fmtPrompt.format("New name", info['name'])
			newName = input(prompt)
			if newName == "":
				newName = info['name']
			print("Your new id is {} and your new name is '{}'".format(newId, newName))
			info.replace({'id': newId, 'name': newName})
	return info
	

def appendNewInfo (info):
	with open(TABLE_PATH, "a") as f:

		f.close()
	print("Done")


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Parse a report URL and add it to the report table.")

	parser.add_argument("-u", "--url", help="ERCOT report url to parse")
	args = parser.parse_args()
	print(args)
	sUrl = args.url
	print("sUrl=" + sUrl)
	info = _getReportUrlInfo.getInfo(sUrl)
	printInfo(info)
	newInfo = askForNewInfo(info)
	appendNewInfo(newInfo)

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

