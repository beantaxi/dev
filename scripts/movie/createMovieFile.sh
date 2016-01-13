#!/bin/bash

### Make the movie & Copy it to dropbox
#<<<<<<< HEAD
#yday=$1
#=======
dt=${1:-"yesterday 13:00"}
yday=$(date -d "$dt" '+%Y%m%d')
#>>>>>>> 2d42677594fa0044f5947381fd6a47ef8d652632
movieName=ercot-map-$yday.avi
ffmpeg -i movie/%03d.png -vf "setpts=4*PTS" $movieName
cp -f $movieName ~/Dropbox/ercot-map-yesterday.avi

