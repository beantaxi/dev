rm movie/*.png
x=1; 
for i in `ls -1dv $PWD/ercot*20150601*.png`; do 
	counter=$(printf %03d $x); 
	echo $i;
	ln -s "$i" movie/"$counter".png; 
	x=$(($x+1)); 
done;

