#!/bin/bash

if [ $# -lt 1 ]; then
	echo Usage: $BASHSOURCE ParentClassName
	exit -1
fi

CLASSNAME=$1
findInPy "class [A-Z][a-zA-Z]\+(.*$CLASSNAME" /usr/local/lib/python3.4/importlib
findInPy "_register($CLASSNAME" /usr/local/lib/python3.4/importlib

