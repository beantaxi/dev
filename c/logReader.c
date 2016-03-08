#define _XOPEN_SOURCE
#include <fcntl.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

void dumpTm (struct tm* tm)
{
	printf("%d/%d/%d %d:%02d:%02d\n", tm->tm_mon+1, tm->tm_mday, tm->tm_year+1900, tm->tm_hour, tm->tm_min, tm->tm_sec);
}

int getCurrentYear ()
{
	time_t t = time(NULL);
	struct tm* tm = localtime(&t);
	int year = tm->tm_year + 1900;

	return year;
}


const time_t getTimeFromLine (const char* line)
{
	const char* fmt = "%b %d %H:%M:%S";
	struct tm tm;
	strptime(line, fmt, &tm);
	tm.tm_year = getCurrentYear() - 1900;
	time_t t = mktime(&tm);

	return t;
}


const time_t getTimeFromArg (const char* arg)
{
	const char* fmt = "%b %d %H%M";
	struct tm tm;
	memset(&tm, 0, sizeof(tm));
	strptime(arg, fmt, &tm);
	tm.tm_year = getCurrentYear() - 1900;
	time_t t = mktime(&tm);

	return t;
}


/*
bool cmpLineToDate (const char* line, const char* date)
{
	if (line == NULL || date == NULL || strlen(line) < 15)
	{
		return 0;
	}

//	int d, h, mi, s;
//	sscanf(line, "%3s %2d %2d:%2d:%2d", mo, &d, &h, &mi, &s);
//	printf("%s %d %d %d %d\n", mo, d, h, mi, s);
	struct tm tm;
	getTmFromLine(line, &tm);

}
*/

int main (int argc, char* argv[])
{
	char* line = NULL;				// getline handles allocation if you give it NULL
	size_t n;

	time_t tArg = getTimeFromArg(argv[1]);
	while (getline(&line, &n, stdin) != -1)
	{
		time_t tLine = getTimeFromLine(line);
		if (tLine >= tArg)
		{
			printf("%s", line);		// getline includes trailing \n
			free(line);					// and it malloc's line
			line = NULL;				// and handles allocation if we give it NULL
		}
	}

/*
	char* arg = argv[1];
	puts(arg);

	//const char* fmt = "%b %d %H%M";
	const char* fmt = "%b %d %H%M";
	struct tm tm;
	memset(&tm, 0, sizeof(tm));
	const char* r = strptime(arg, fmt, &tm);
	printf("rc=%s\n", r);
	tm.tm_year = getCurrentYear() - 1900;
	dumpTm(&tm);
	printf("tm=%s\n", asctime(&tm));
	
	time_t t = mktime(&tm);
	printf("t=%s\n", ctime(&t));
*/

	return 0;
}
