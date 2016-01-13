#!/bin/bash
### Create 001.png, 002.png etc symlinks for all those files
mkdir -p movie
#<<<<<<< HEAD
#rm -r movie/*
#=======
find movie -mindepth 1 -delete
#>>>>>>> 2d42677594fa0044f5947381fd6a47ef8d652632
x=1;
for f in `ls -1dv $yday*with-timestamp.png`; do
	counter=$(printf %03d $x);
	echo $f;
	ln -s "../$f" movie/$counter.png;
	x=$(($x+1));
done;
