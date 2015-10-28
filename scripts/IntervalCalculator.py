import datetime
from enum import Enum
import logging
import statistics
import time
import X

class IntervalEnum(Enum):
	DAILY = 86400
	HOURLY = 3600
	FIVE_MINUTES = 300

class IntervalCalculator:
	@staticmethod
	def getInterval (deltas):
		intervalMap = {IntervalEnum.DAILY: 0, IntervalEnum.HOURLY: 0, IntervalEnum.FIVE_MINUTES: 0}
		keys = intervalMap.keys()
		for delta in [delta.total_seconds() for delta in deltas]:
			for key in keys:
				if delta >= key.value*0.95 and delta <= key.value*1.05:
					intervalMap[key] += 1
		keyWithMost = None
		for key, val in intervalMap.items():
			if val >= 0.8*len(deltas):
				keyWithMost = key
				break
		return keyWithMost

	@classmethod
	def getTrickySeconds (delta):
		pass
		

	@staticmethod
	def _getDailyStartTime (dtReport):
		# Get the average
		# Chuck outliers
		# Get the average again
		avg = statistics.mean([delta.total_seconds() for delta in deltas])
		logging.debug("avg=" + str(avg))
		for delta in deltas:
			print("{:5}{:10}{:24}{:24}".format(str(delta.days), str(delta.seconds), str(avg), str(abs(delta.total_seconds()-avg))))
		avg2 = statistics.mean([delta.total_seconds() for delta in deltas if abs(delta.total_seconds()-avg) < 7200])
		logging.debug("avg2=" + str(avg2))
		startTime = time.gmtime(avg2)
		return startTime
