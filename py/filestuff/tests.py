import glob
import os
import re
import sys

def archiveExtracts (extractsFolder, archiveFolder):
	if not os.path.isdir(extractsFolder):
		raise Exception("Invalid extractsFolder: " + extractsFolder)
	if not os.path.isdir(archiveFolder):
		raise Exception("Invalid archiveFolder: " + archiveFolder)
	pass
	dateFolders = getDateFolders(extractsFolder)
	for dateFolder in dateFolders:
		basename = os.path.basename(dateFolder)
		tarName = basename + ".tar"
		tarPath = os.path.join(archiveFolder, tarName)
		gzPath = tarPath + ".gz"
		print(tarPath)
		print(gzPath)


def getDateFolders (extractsFolder):
	filespec = os.path.join(extractsFolder, '*')
	files = glob.glob(filespec)
	dateFolders = [f for f in files if isDateFolder(f)]
	return dateFolders

def isDateFolder (f):
	isDate = re.search("\d{8}", os.path.basename(f))
	isFolder = os.path.isdir(f)
	flag = isDate and isFolder
	return flag
	

if __name__ == '__main__':
	extractsFolder = sys.argv[1]
	archiveFolder = sys.argv[2]
	archiveExtracts(extractsFolder, archiveFolder)

