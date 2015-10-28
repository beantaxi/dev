#!/bin/bash

dt=$(date -d "today" +%Y%m%d)
mkdir -p ~euclid/contourMaps/$dt
cp -n -v -t ~euclid/contourMaps/$dt ~euclid/contourMaps/$dt*.kml ~euclid/contourMaps/$dt*.png

