#!/bin/bash
function doFile
{
	imageFile=$1
	imageFilename=${imageFile%.*}
	year=$(echo $i | cut -c1-4)
	month=$(echo $i | cut -c5-6)
	day=$(echo $i | cut -c7-8)
	hour=$(echo $i | cut -c10-11)
	minute=$(echo $i | cut -c12-13)
	timestampFilename="${imageFilename}-timestamp.png"
#	echo "$year $month $day $hour $minute"
	echo Timestamping $imageFile to $timestampFilename ...
	convert -size 600x600 xc:transparent -font Courier-bold -pointsize 25 -fill skyblue -draw "text 10,33 '$year $month $day'" -draw "text 10, 68 '$hour:$minute'" $timestampFilename
	composite -quality 100 $timestampFilename $imageFile ${imageFilename}-with-timestamp.png
}

#rm *timestamp*.png;
for i in `ls -1dv *.png`; do 
	doFile $i;
done;

