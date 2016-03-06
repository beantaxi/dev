#include <fcntl.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>


bool cmpLineToDate (const char* line, const char* date)
{
	if (line == NULL || date == NULL || strlen(line) < 15)
	{
		return 0;
	}

	char mo[10];
	int d, h, mi, s;
	sscanf(line, "%3s %2d %2d:%2d:%2d", mo, &d, &h, &mi, &s);
	printf("%s %d %d %d %d\n", mo, d, h, mi, s);
}


int main (int argc, char* argv[])
{
	char* line = NULL;
	size_t n;
	const char* SYSLOG = "/var/log/syslog";
	FILE* f;

	f = fopen(SYSLOG, "r");
	printf("f=%p\n", f);
	while (getline(&line, &n, f) != -1)
	{
		if (cmpLineToDate(line, "") >= 0)
		{
			printf("%s", line);
			free(line);
			line = NULL;
		}
	}
	puts("");
	perror("Done reading file");

	return 0;
}
