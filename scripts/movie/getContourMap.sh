#!/bin/bash

# This could all be a single clever command. But then I would never be able to read it.
py=~ubuntu/dev/py/venv/main/bin/python3

URL_html=http://www.ercot.com/content/cdr/contours/rtmLmpHg.html
URL_kml=http://www.ercot.com/content/cdr/contours/rtmLmpHg.kml
URL_png=http://www.ercot.com/content/cdr/contours
script=~euclid/scripts/getCounterMap2.py

# Get the filename base, which consists of rounding off current time to the most recent 5 min interval
filename=$($py $script "$(date)")
# Extract the PNG filename from the HTML, and then get the PNG
imgsrc=$(wget -O - $URL_html | $py ~euclid/scripts/extractPngUrl.py)
wget -O $filename.png $URL_png/$imgsrc
# Get the KML
wget -O $filename.kml $URL_kml
