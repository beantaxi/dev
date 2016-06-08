#include <fcntl.h>
#include <stdio.h>
#include <string.h>
#include <sys/epoll.h>
#include "socketLib.h"


void testNewStringFunctions ()
{
	const char* line = "HTTP/1.1 200 OK";
	const char* token = " ";
	const char* s;
	int n;

	s = line;
	
	// HTTP/1.0
	puts(s);
	n = strcspn(s, " ");
	fwrite(s, n, 1, stdout);
	puts("");
	s = s+n+1;

	// 200
	puts(s);
	n = strcspn(s, " ");
	fwrite(s, n, 1, stdout);
	puts("");
	s += n+1;

	// OK
	puts(s);
	n = strcspn(s, " ");
	fwrite(s, n, 1, stdout);
	puts("");
	s += n+1;

	printf("\n");
}

int stringToFile (const char *s, const char* path)
{
	FILE* outfile = fopen(path, "w");
	fwrite(s, strlen(s), 1, outfile);
	fclose(outfile);
	int fdIn = open(path, O_RDONLY);
	return fdIn;
}

void testReadUntil ()
{
	const char* s;
	const char* delim;

	s= "HTTP/1.1 200 OK\r\n";
	in = stringToFile(s, "test.txt");
	
	delim = " ";
	puts(readUntil(in, delim));
	puts(readUntil(in, delim));

	delim = "\r\n";
	puts(readUntil(in, delim));

	const char* lastThingee = readUntil(in, delim);
	if (lastThingee == NULL)
	{
		puts("lastThingee is null");
	}
	else
	{
		puts(lastThingee);
	}
}


void checkEPollRdHupValue ()
{
	printf("EPOLLRDHUP=%d\n", EPOLLRDHUP);
}

int main (int argc, char* args[])
{
	testReadUntil();

	return 0;
}


