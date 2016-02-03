#include <stdio.h>
#include <string.h>

int main (int argc, char* args[])
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
	return 0;
}
