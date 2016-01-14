#include <poll.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/inotify.h>
#include <sys/ioctl.h>

const char* PATH = "/tmp/pub/";

void onRead (int fd, int nToRead)
{
	int rc;

	printf("%d byte(s) to read!\n", nToRead);
	char* buf = malloc(nToRead);
	read(fd, buf, nToRead);
	if (rc == -1)
	{
		perror("Error on read()");
		exit(EXIT_FAILURE);
	}
	struct inotify_event* ev = (struct inotify_event*)buf;
	printf("wd=%d\n", ev[0].wd);
	printf("mask=%d\n", ev[0].mask);
	printf("cookie=%d\n", ev[0].cookie);
	printf("len=%d\n", ev[0].len);
	printf("name=%s\n", ev[0].name);

	const char* pyPath = "/home/ubuntu/dev/py/venv/main/bin/python3";
	const char* scriptPath = "/home/ubuntu/work/euclid/scripts/sendSns.py";
	char* args = ev[0].name;
	char cmd[255];
	sprintf(cmd, "%s %s %s", pyPath, scriptPath, args);
	system(cmd);
}


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
	
	int wd = inotify_add_watch(fd, PATH, IN_CREATE | IN_MODIFY);
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
	
	onRead(pfd.fd, nToRead);
	
	rc = inotify_rm_watch(fd, wd);
	if (rc == -1)
	{
		perror("Error with inotify_add_watch");
		exit(EXIT_FAILURE);
	}
	
	close(fd);
}
