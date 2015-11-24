import config
import logging
import os.path
import urllib.request
import _utils
import Constants
from ExtractStore import ExtractStore
from ExtractTable import ExtractTable

def createExtractStore ():
	table = createExtractTable()
	store = ExtractStore(table, config.DOWNLOAD_FOLDER)
	return store

def createExtractTable ():
	table = ExtractTable(Constants.TABLE_PATH, Constants.BACKUP_TABLE_PATH, Constants.TEMP_TABLE_PATH)
	return table

def installOpener ():
	httpsHandler = _utils.createHttpsHandler(clientCertPath=config.clientCertPath, caCertPath=config.caCertPath)
	cookieProcessor = _utils.createCookieProcessor()
	opener = urllib.request.build_opener(httpsHandler, cookieProcessor)
	urllib.request.install_opener(opener)

installOpener()
logging.basicConfig(level=logging.DEBUG)



