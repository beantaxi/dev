#!/bin/bash

### Create a directory for yesterdays files, and mv them there
#<<<<<<< HEAD
#yday=$1
#=======
dt=${1:-"yesterday 13:00"}
yday=$(date -d "$dt" '+%Y%m%d')
#>>>>>>> 2d42677594fa0044f5947381fd6a47ef8d652632
echo "Creating/emptying $yday ..."
mkdir -p $yday
rm -r $yday/*
echo "Moving PNG files ..."
mv $ $yday*.png $yday
echo "Moving KML files ..."
mv $yday*.kml $yday

#<<<<<<< HEAD
#=======
ln -s $(pwd -P)/$yday /www/png/$yday
#>>>>>>> 2d42677594fa0044f5947381fd6a47ef8d652632
