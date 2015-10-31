import colorama
import logging
import os.path
import urllib.request
import sys
import _utils
import config

LISTINGS_FOLDER = os.path.join(config.DOWNLOAD_FOLDER, 'listings')
TABLE_NAME = 'ercotReportTable.txt'  
BACKUP_TABLE_NAME = TABLE_NAME + '.bak'
TEMP_TABLE_NAME = TABLE_NAME + '.tmp' 
BACKUP_TABLE_PATH = os.path.join(config.TABLE_FOLDER, BACKUP_TABLE_NAME)
TABLE_PATH = os.path.join(config.TABLE_FOLDER, TABLE_NAME)
TEMP_TABLE_PATH = os.path.join(config.TABLE_FOLDER, TEMP_TABLE_NAME)

def installOpener ():
	clientCertPath = _utils.getCertPath(config.clientCertFile)
	caCertPath = _utils.getCertPath(config.caCertFile)
	httpsHandler = _utils.createHttpsHandler(clientCertPath=clientCertPath, caCertPath=caCertPath)
	cookieProcessor = _utils.createCookieProcessor()
	opener = urllib.request.build_opener(httpsHandler, cookieProcessor)
	urllib.request.install_opener(opener)

installOpener()
logging.basicConfig(level=logging.DEBUG)
colorama.init(autoreset=True)
