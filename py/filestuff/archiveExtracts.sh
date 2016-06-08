#!/bin/bash

function getExtractFolders ()
{
	extractsHome=$1
	find "$extractsHome" -type d -name '????????' -regextype grep -regex ".*/[0-9]\{8\}$" -print
}

function oldStuff 
{
# Get list of date folders
extractFolders=$(find "$extractsHome" -type d -name '????????' -regextype grep -regex ".*/[0-9]\{8\}$")

for f in $extractFolders; do
	basename="${f##*/}"
	tarName="$basename.tar"
	tarPath="$archiveHome/$tarName"
	gzPath="$tarPath.gz"
	# echo tarPath=$tarPath
	if [ -f $gzPath ]; then
		echo "Unzipping $gzPath ..."
		gunzip "$gzPath"
	fi
	echo "Creating/appending to $tarPath ..."
	(cd "$extractsHome"; tar --append -f "$tarPath" $basename/cdr*.zip)
	echo "Gzipping $tarPath ..."
	gzip "$tarPath"
done
}


if [ $# -lt 2 ]; then
	>&2 echo "Usage:   $BASH_SOURCE extractsHome archiveHome"
	>&2 echo "Example: $BASH_SOURCE /data/downloads/extracts /data/archive/extracts"
	exit -1
fi

extractsHome=$1
archiveHome=$2

if [ ! -d $extractsHome ]; then
	echo "'$extractsHome' not a valid extracts home folder"
	exit -1
fi

if [ ! -d $archiveHome ]; then
	>&2 echo "'$archiveHome' not a valid archive home folder"
	>&2 exit -1
fi
# For each dateFolder,
#    Create the archive gunzip name
#    If it exists,
#       Gunzip the archive
#    Append files to archive, removing them I guess
#    gzip the archive

