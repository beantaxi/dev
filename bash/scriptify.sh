#!/bin/bash

SteelyDan_Album_ShowBizKids='spotify:album:6OiTM5PNqUE6FafIoR4xnF'
Nrbq_Track_WeTravelTheSpaceways='spotify:track:0jv1y12hwJhHEYdbmyJRWP'
VA_Playlist_CoffeehouseJazzVol2='spotify:album:17bhbh3BUa0QciL71PFcJz'

VA_Chill='spotify:album:17vHPMmoxN5B8cdhCDeMTe'
VA_Blast='spotify:user:1230186738:playlist:6QaHXC4J18RpJrBJPnai7t'

conn=org.mpris.MediaPlayer2.spotify
obj=/org/mpris/MediaPlayer2
inf=org.mpris.MediaPlayer2.Player


blast () { choose VA_Blast; }
chill () { choose VA_Chill; }

choose ()
{
	if [[ $# -lt 1 ]]; then
		echo "Usage:   choose spotifyUri"
		echo "Example: choose 'spotify:album:6OiTM5PNqUE6FafIoR4xnF'"
		return 1
	fi

	if [[ ${1:0:7} == 'spotify' ]]; then
		uri="string:$1"
	else
		uri="string:${!1}"
	fi
	dbusSend OpenUri "$uri"
}



play ()
{
	dbusSend Play
}


pause ()
{
	dbusSend Pause
}


dbusSend ()
{
	if [[ $# -lt 1 ]]; then
		echo "Usage:   dbusSend command [args]"
		echo "Example: dbusSend Play"
		echo "Example: dbusSend OpenUri 'spotify:album:6OiTM5PNqUE6FafIoR4xnF'"
		return 1
	fi

	api=$1
	args=${@:-2}
	echo api=$api
	echo args=$args
	if [[ -z $args ]]; then
		dbus-send --print-reply --dest="$conn" "$obj" "$inf.$api"
	else
		dbus-send --print-reply --dest="$conn" "$obj" "$inf.$api" "$args"
	fi
}
