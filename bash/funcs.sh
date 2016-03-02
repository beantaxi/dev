#!/bin/bash

newScript ()
{
	touch $1
	chmod 744 $1
	echo -e '#!/bin/bash\n\n' > $1
	vi + -c'startinsert' $1
}
