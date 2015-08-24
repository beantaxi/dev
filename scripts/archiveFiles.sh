#!/bin/bash

whichDate=$1
echo whichDate=$whichDate
dt=$(date --date "$whichDate" +%Y%m%d)
echo dt=$dt
tar czf $dt.tar.gz $dt --remove-files
