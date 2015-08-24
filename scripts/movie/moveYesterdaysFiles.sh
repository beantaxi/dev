#!/bin/bash

### Create a directory for yesterdays files, and mv them there
dt=${1:-"yesterday 13:00"}
yday=$(date -d "$dt" '+%Y%m%d')
echo "Creating/emptying $yday ..."
mkdir -p $yday
rm -r $yday/*
echo "Moving PNG files ..."
mv $ $yday*.png $yday
echo "Moving KML files ..."
mv $yday*.kml $yday

ln -s $(pwd -P)/$yday /www/png/$yday
