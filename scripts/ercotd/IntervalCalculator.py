import datetime
from enum import Enum
import statistics
import time

class IntervalEnum(Enum):
	DAILY = 86400
	HOURLY = 3600
	FIVE_MINUTES = 300
	FIFTEEN_MINUTES = 900

	@classmethod
	def fromstring (cls, s):
		return cls._member_map_[s]

	def tostring (self):
		for k,v in self.__class__._member_map_.items():
			if v == self:
				return k

class IntervalCalculator:
	@classmethod
	def createClearIntervalMap (cls):
		intervalMap = {}
		for k in IntervalEnum:
			intervalMap[k] = 0
		return intervalMap
		

	@classmethod
	def getInterval (cls, deltas):
		intervalMap = cls.createClearIntervalMap()
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
	def _getDailyStartTime (dtExtract):
		# Get the average
		# Chuck outliers
		# Get the average again
		avg = statistics.mean([delta.total_seconds() for delta in deltas])
		X.debug("avg=" + str(avg))
		for delta in deltas:
			print("{:5}{:10}{:24}{:24}".format(str(delta.days), str(delta.seconds), str(avg), str(abs(delta.total_seconds()-avg))))
		avg2 = statistics.mean([delta.total_seconds() for delta in deltas if abs(delta.total_seconds()-avg) < 7200])
		X.debug("avg2=" + str(avg2))
		startTime = time.gmtime(avg2)
		return startTime
