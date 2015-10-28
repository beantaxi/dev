#!/bin/bash
### Create 001.png, 002.png etc symlinks for all those files
mkdir -p movie
rm -r movie/*
x=1;
for f in `ls -1dv $yday*with-timestamp.png`; do
	counter=$(printf %03d $x);
	echo $f;
	ln -s "../$f" movie/$counter.png;
	x=$(($x+1));
done;
