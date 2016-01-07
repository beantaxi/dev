import datetime
import math

class TimeDelta2 (datetime.timedelta):

	@classmethod
	def _getFields (cls, delta):
		SECONDS_PER_DAY = 86400
		s = delta.days * SECONDS_PER_DAY + delta.seconds
		d, s = cls._normalize(s, SECONDS_PER_DAY)
		h, s = cls._normalize(s, 3600)
		m, s = cls._normalize(s, 60)
		fields = {'days': d, 'hours': h, 'minutes': m, 'seconds': s}
		return fields

	@classmethod
	def _normalize (cls, seconds, n):
		x = int(seconds/n)
		s = seconds - x*n
		if abs(s) > n/2:
			x += int(math.copysign(1, s))
			s -= int(math.copysign(n, s))
		return (x, s)

	@classmethod
	def toString (cls, delta):
		if delta == datetime.timedelta(0):
			sDelta = "0"
		else:
			sDelta = ""
			fields = TimeDelta2._getFields(delta)
			if fields['days']:
				sDelta += "{}d ".format(fields['days'])
			if fields['hours']:
				sDelta += "{:>3}h ".format(fields['hours'])
			if fields['minutes']:
				sDelta += "{:>3}m ".format(fields['minutes'])
			if fields['seconds']:
				sDelta += "{:>3}s ".format(fields['seconds'])
			sDelta = sDelta.strip()
		return sDelta
	
	def __str__ (self):
		return TimeDelta2.toString(self)
