from datetime import datetime
from datetime import timedelta


def printThumbnailLine (dt):
	imgPath = dt.strftime("http://sissy/euclid/img/%Y%m%d/%Y%m%d-%H%M.png")
	alt = dt.strftime("%H%M")
	print("\t<td class='thumbnail'><img width=25 src='" + imgPath + "' alt='" + alt + "'/> </td>");

dt = datetime(2015, 6, 23, 0, 0)
dtCurr = dt
delta = timedelta(minutes=5)
while dtCurr.day <= dt.day:
	if dtCurr.minute == 0:
		print "<tr>"
	printThumbnailLine(dtCurr)
	if dtCurr.minute == 55:
		print "</tr>"
	dtCurr = dtCurr + delta



	

	
