#include <poll.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/inotify.h>
#include <sys/ioctl.h>


int main ()
{
	int rc;		// generic return code from various functions

	// Watch for movie file being created
	int fd = inotify_init();
	if (fd == -1)
	{
		perror("Error with inotify_init()");
		exit(EXIT_FAILURE);
	}
	
	const char* path = "/home/chrissy/Dropbox/euclid/pub";
	int wd = inotify_add_watch(fd, path, IN_CREATE | IN_MODIFY);
	if (wd == -1)
	{
		perror("Error with inotify_add_watch()");
		exit(EXIT_FAILURE);
	}

	// poll until there is something left to read.
	// This is necessary because we will be reading a variable number of bytes
	// (eg the name of the file)
	struct pollfd pfd;
	pfd.fd = fd;
	pfd.events = POLLIN;
	rc = poll(&pfd, 1, -1);
	if (rc == -1)
	{
		perror("Error with poll()");
		exit(EXIT_FAILURE);
	}

	// Since there is something to read, get the byte count
	int nToRead;
	rc = ioctl(pfd.fd, FIONREAD, &nToRead);
	if (rc == -1)
	{
		perror("Error with ioctl()");
		exit(EXIT_FAILURE);
	}
	printf("%d byte(s) to read!", nToRead);

	rc = inotify_rm_watch(fd, wd);
	if (rc == -1)
	{
		perror("Error with inotify_add_watch");
		exit(EXIT_FAILURE);
	}
	
	close(fd);
}
