#!/bin/bash

newScript ()
{
	local filename="$1"
	touch $filename
	chmod 744 $filename
	echo -e '#!/bin/bash\n\n' > $filename

	checkNoVim "$@"
	if [ $? -eq 0 ]; then
		vi + -c'startinsert' $filename
	fi
}

checkNoVim ()
{
	local optionString='n'
	local args=$(getopt -o $optionString --long novim -n "$BASH_SOURCE" -- "$@")
	eval set -- "$args"
	if [ $1 = '-n' ] || [ $1 = '--novim' ]; then
		return 1
	else
		return 0
	fi
}
