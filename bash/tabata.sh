#!/bin/bash

source $(getdir "$BASH_SOURCE")/scriptify.sh || exit


bye ()
{
	say Goodbye
	choose $nrbq_we-travel-the-spaceways
	play
} 


say ()
{
	words="$1"
	espeak -a 200 -s 200 "$words"
	echo "$words"
}


takeABreak ()
{
	say Stop
	choose "$BREAKSONG"
	play
}


workSprint ()
{
	say GO
	choose "$WORKSONG"
	play
}




trap 'rc=$?; bye; exit $rc' SIGINT
trap 'rc=$?; bye; exit $rc' SIGTERM

if [[ $# -lt 2 ]]; then
	echo "Usage: $BASH_SOURCE workTimeInSeconds playTimeInseconds [loop]"
	echo "Example: $BASH_SOURCE 600 300       # 10 minutes work, 5 minute break"
	echo "Example: $BASH_SOURCE 600 300 loop  # 10 minutes work, 5 minutes break, infinite loop"
	exit -1
fi

echo $1 $2
workTime=$(($1*60))
playTime=$(($2*60))
loop=${3:-""}

while true; do
	workSprint
	sleep $workTime
	takeABreak
	sleep $playTime
	if [[ -z $loop ]]; then break; fi	
done
bye
