import sys
import X
from ExtractStore import ExtractStore

if __name__ == "__main__":
	idExtract = sys.argv[1]
	store = X.createExtractStore()
	path = store.downloadLatestExtract(idExtract)
