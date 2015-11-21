import os.path
import config

LISTINGS_FOLDER = os.path.join(config.DOWNLOAD_FOLDER, 'listings')
TABLE_NAME = 'ercotExtractTable.txt'  
BACKUP_TABLE_NAME = TABLE_NAME + '.bak'
TEMP_TABLE_NAME = TABLE_NAME + '.tmp' 
BACKUP_TABLE_PATH = os.path.join(config.TABLE_FOLDER, BACKUP_TABLE_NAME)
TABLE_PATH = os.path.join(config.TABLE_FOLDER, TABLE_NAME)
TEMP_TABLE_PATH = os.path.join(config.TABLE_FOLDER, TEMP_TABLE_NAME)
