#!/bin/bash

datespec=${1:-"yesterday 13:00"}
dt=$(date -d "$datespec" +%Y%m%d)
moviePath=$dt/ercot-map-$dt.avi
cp -v -f $moviePath ~/Dropbox/ercot-map-yesterday.avi


