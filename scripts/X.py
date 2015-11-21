import logging
import os.path
import urllib.request
import _utils

DOWNLOAD_FOLDER = '/tmp/downloads/ercot'
TABLE_FOLDER = '/home/chrissy/work/euclid/scripts'
LISTINGS_FOLDER = os.path.join(DOWNLOAD_FOLDER, 'listings')
TABLE_NAME = 'ercotExtractTable.txt'  
BACKUP_TABLE_NAME = TABLE_NAME + '.bak'
TEMP_TABLE_NAME = TABLE_NAME + '.tmp' 
BACKUP_TABLE_PATH = os.path.join(TABLE_FOLDER, BACKUP_TABLE_NAME)
TABLE_PATH = os.path.join(TABLE_FOLDER, TABLE_NAME)
TEMP_TABLE_PATH = os.path.join(TABLE_FOLDER, TEMP_TABLE_NAME)

certPath = "/home/chrissy/.ssh/ercot-mis-client-and-pk.pem" 
caPath = "/home/chrissy/.ssh/ercot-mis-ca.pem"

def installOpener ():
	httpsHandler = _utils.createHttpsHandler(certPath=certPath, caPath=caPath)
	cookieProcessor = _utils.createCookieProcessor()
	opener = urllib.request.build_opener(httpsHandler, cookieProcessor)
	urllib.request.install_opener(opener)

installOpener()
logging.basicConfig(level=logging.DEBUG)



