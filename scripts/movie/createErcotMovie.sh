#!/bin/bash
### Create a directory for yesterdays files, and mv them there

function moveYesterdaysFiles ()
{
	echo "Creating/emptying $yday ..."
	mkdir -p $yday
	rm -r $yday/*
	echo "Moving PNG files ..."
	mv $ $yday*.png $yday
	echo "Moving KML files ..."
	mv $yday*.kml $yday
}

function timestampPngs
{
	for i in `ls -1dv $yday/$yday*.png`; do 
		echo $i
		# Parse datetime from filename
		imageFile=$i
		imageFilename=${imageFile%.*}
		year=$(echo $i | cut -c0-4)
		month=$(echo $i | cut -c5-6)
		day=$(echo $i | cut -c7-8)
		hour=$(echo $i | cut -c10-11)
		minute=$(echo $i | cut -c12-13)
		timestampFilename="$year$month$day-$hour$minute-timestamp.png"
		echo Timestamping $imageFile ...
		# Create a PNG containing the timestamp as text
		convert -size 600x600 xc:transparent -font Courier-bold -pointsize 25 -fill Blue -draw "text 10,33 '$year $month $day'" -draw "text 10, 68 '$hour:$minute'" $yday/$timestampFilename
		# Combine the original countour map PNG, and the timestamp PNG, to make a timestamped countourMap

	composite -quality 100 $yday/$timestampFilename $yday/$imageFile $yday/${imageFilename}-with-timestamp.png
done;

}


function createSequenceSymlinks ()
{
	### Create 001.png, 002.png etc symlinks for all those files
	mkdir -p movie
	rm -r movie/*
	x=1;
	for i in `ls -1dv $yday/$yday*with-timestamp.png`; do
	   counter=$(printf %03d $x);
	   echo $i;
	   ln -s "$i" movie/"$counter".png;
	   x=$(($x+1));
done;
}


function createMovie ()
{
	### Make the movie & Copy it to dropbox
	movieName=ercot-map-$yday.avi
	ffmpeg -i $yday/movie/%03d.png -vf "setpts=4*PTS" $yday/$movieName
	cp -f $yday/$movieName ~/Dropbox/ercot-map-yesterday.avi
}


dt=$1
echo dt=$dt
dir="$( cd "$(dirname "$0")" ; pwd -P )"
echo "dir=$dir"
yday=$(date -d "$dt" '+%Y%m%d')
. $dir/moveYesterdaysFiles.sh $yday
pushd `pwd`
cd $yday
. $dir/timestampPngs.sh
. $dir/createSequenceSymlinks.sh
. $dir/createMovieFile.sh $yday
popd
