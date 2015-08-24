for i in $(ls -1v *.png | grep -v timestamp); do stub=${i%.*}; convert $i -resize 50x50 $stub-small.png; done;
