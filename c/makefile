CFLAGS="-std=c99 -D_POSIX_C_SOURCE=200809L -g"

getdir: getdir.c
	sudo cp getdir.c /usr/local/src
	sudo gcc -o /usr/local/bin/getdir /usr/local/src/getdir.c


movieWatcher: movieWatcher.c
	gcc -o movieWatcher ini.c movieWatcher.c

socketReader: socketReader.c socketReader.h makefile
	gcc "$(CFLAGS)" -o socketReader socketReader.c
