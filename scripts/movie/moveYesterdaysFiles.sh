#!/bin/bash

### Create a directory for yesterdays files, and mv them there
yday=$1
echo "Creating/emptying $yday ..."
mkdir -p $yday
rm -r $yday/*
echo "Moving PNG files ..."
mv $ $yday*.png $yday
echo "Moving KML files ..."
mv $yday*.kml $yday

