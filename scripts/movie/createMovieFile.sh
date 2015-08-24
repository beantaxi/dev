#!/bin/bash

### Make the movie & Copy it to dropbox
dt=${1:-"yesterday 13:00"}
yday=$(date -d "$dt" '+%Y%m%d')
movieName=ercot-map-$yday.avi
ffmpeg -i movie/%03d.png -vf "setpts=4*PTS" $movieName
cp -f $movieName ~/Dropbox/ercot-map-yesterday.avi

