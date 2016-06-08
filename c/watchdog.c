#include <errno.h>
#include <limits.h>
#include <poll.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/ioctl.h>
#include <sys/inotify.h>
#include <unistd.h>

#define EVENT_SIZE (sizeof(struct inotify_event))
#define EVENT_BUF_LEN (1024*(EVENT_SIZE+16))

#define errorCheck(s) if (rc == -1) perror(s)

/*******************************************************
 *
 * Reading iNotify events is tricky. The structure itself
 * is dynamically sized - the name field is whatever the
 * name of the file is, so of course it can be any length
 * (up to the system-defined limit for filesizes.)
 *
 * This means you can't just do a blocking read(), because you
 * don't know how many bytes you need to read, and so you don't
 * know how many bytes you have to allocate. And we're trying
 * to be efficient here :)
 *
 * Safely getting an iNotify event requires 3 steps:
 * 1. poll() the inotify fd, with infinite timeout (wait for something to read)
 * 2. ioctl() to get the number of bytes available to be read
 * 3. Allocate a char* buffer and read() the proper number of bytes into the buffer.
 *
 * If this works, cast the char* into a struct inotify_event* and return it.
 q*
 * This function dynamically allocates the storage for the event. It is the responsibility
 * of the caller to free the allocated memory.
 */
struct inotify_event* getNotifyEvent (int fd)
{
	int rc;

	// poll() on the inotify fd, to wait for an event
	struct pollfd pfd;
	pfd.fd = fd;
	pfd.events = POLLIN;
	rc = poll(&pfd, 1, -1);
	errorCheck("poll()");

	// ioctl() to get the number of bytes to read
	unsigned int nToRead;
	rc = ioctl(fd, FIONREAD, &nToRead);
	errorCheck("ioctl()");

	// allocate that many bytes and read them
	char* buf = malloc(nToRead);
	rc = read(fd, buf, nToRead);
	errorCheck("read()");

	// cast result & return it
	struct inotify_event* event = (struct inotify_event*)buf;

	return event;
}


void doIt ()
{
	int rc;
	//	puts("Initializing inotify ...");
	//	puts("Waiting for events ...");

	// Call to inotify_init
	//	puts("Getting inotify fd (via inotify_init) ...");
	int fd;
	fd = inotify_init();
	if (fd == -1) { perror("inotify_init()"); }
	else
	{
		// Watch a folder
		const char* PATH = "/tmp/downloads";
		int wd = inotify_add_watch(fd, PATH, IN_ATTRIB | IN_CREATE);
		if (wd == -1) { perror("inotify_add_watch()"); }
		else
		{
			printf("Waiting on something to happen ...");
			struct inotify_event* ev = getNotifyEvent(fd);
			// Print out what happened
			printf("%d %d %d %d %s\n", ev->wd, ev->mask, ev->cookie, ev->len, ev->name);
			puts("(whoa.)");				
			free(ev);

			// Close up shop
			//	puts("Closing inotify fd (w close())");
			rc = inotify_rm_watch(fd, wd);
			if (rc == -1) { perror("inotify_rm_watch()"); }
		}
		
		rc = close(fd);
		if (rc == -1) { perror("close()"); }
	}

	//	puts("Done.");
}


void main ()
{
	int LIMIT = 1000000;

	for (int i=0; i<LIMIT; ++i)
	{
		printf("%d\n", i);
		doIt();
	}
}
