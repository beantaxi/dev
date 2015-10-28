#!/bin/bash

### Make the movie & Copy it to dropbox
yday=$1
movieName=ercot-map-$yday.avi
ffmpeg -i movie/%03d.png -vf "setpts=4*PTS" $movieName
cp -f $movieName ~/Dropbox/ercot-map-yesterday.avi

