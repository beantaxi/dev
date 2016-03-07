CFLAGS=-std=c99 -D_POSIX_C_SOURCE=200809L -g

getdir: getdir.c
	sudo cp getdir.c /usr/local/src
	sudo gcc -o /usr/local/bin/getdir /usr/local/src/getdir.c

movieWatcher: movieWatcher.c
	gcc -o movieWatcher ini.c movieWatcher.c

logReader: logReader.c
	gcc $(CFLAGS) -o logReader logReader.c

socketLib: socketLib.c socketLib.h 
	gcc $(CFLAGS) -c socketLib.c

socketReader: socketReader.c socketLib.o
	gcc "$(CFLAGS)" -o socketReader socketReader.c socketLib.o

socketPoller: socketPoller.c socketLib.o
	gcc $(CFLAGS) -o socketPoller socketPoller.c socketLib.o

test: test.c socketLib
	gcc $(CFLAGS) -o test test.c socketLib.o

