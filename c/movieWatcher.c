#include <poll.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <syslog.h>
#include <sys/inotify.h>
#include <sys/ioctl.h>
#include "ini.h"


typedef struct
{
	char* watchedPath;
	char* pythonPath;
	char* scriptPath;
} config;


void onRead (int fd, int nToRead, config* cfg)
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

	char msg[255];
	openlog(NULL, LOG_CONS | LOG_PID | LOG_NDELAY, LOG_LOCAL1);
	syslog(LOG_INFO, "File changed: %s\n", ev[0].name);
	closelog();


	char* args = ev[0].name;
	char cmd[255];
	sprintf(cmd, "%s %s %s", cfg->pythonPath, cfg->scriptPath, args);
	printf("cmd=%s\n", cmd);
	system(cmd);
}


int configHandler (void* user, const char* section, const char* name, const char* value)
{
	#define MATCH(s, n) strcmp(section, s) == 0 && strcmp(name, n) == 0
	config* cfg = (config*)user;

	printf("section=%s name=%s value=%s\n", section, name, value);
	if (MATCH("default", "watchedPath"))
	{
		puts("Matched watchedPath");
		cfg->watchedPath = strdup(value);
	}
	else if (MATCH("default", "pythonPath"))
	{
		puts("Matched pythonPath");
		cfg->pythonPath = strdup(value);
	}
	else if (MATCH("default", "scriptPath"))
	{
		puts("Matched scriptPath");
		cfg->scriptPath= strdup(value);
	}

	return 0;
}


int main ()
{
	int rc;		// generic return code from various functions
	
	const char* configFile = "movieWatcher.ini";
	config cfg;
	rc = ini_parse(configFile, configHandler, &cfg);
	if (rc < 0)
	{
		perror("Error on ini_parse()");
		exit(EXIT_FAILURE);
	}


	// Watch for movie file being created
	int fd = inotify_init();
	if (fd == -1)
	{
		perror("Error with inotify_init()");
		exit(EXIT_FAILURE);
	}
	
	printf("watchedPath=%s\n", cfg.watchedPath);
	int wd = inotify_add_watch(fd, cfg.watchedPath, IN_CREATE | IN_MODIFY);
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
	
	onRead(pfd.fd, nToRead, &cfg);
	
	rc = inotify_rm_watch(fd, wd);
	if (rc == -1)
	{
		perror("Error with inotify_add_watch");
		exit(EXIT_FAILURE);
	}
	
	close(fd);
}
