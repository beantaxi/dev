#!/bin/bash

extractTable='/home/euclid/data/ercotExtractTable.txt'
sDate=$(date +%Y%m%d)
bigCmd="ls -lct /home/euclid/data/downloads/$sDate/*cdr.000@*.zip | head --lines=1 | tr -s ' ' | cut -d' ' -f6,7,8,9"

cut -d, -f1 ${extractTable} | tr -d \" | sort | xargs -n1 -I@ sh -c "${bigCmd}"
