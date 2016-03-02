#include <stdlib.h>
#include <stdio.h>
#include "socketLib.h"


void doIt ()
{
	const char* const hostname = "euclid.ooc2000.com";
	int port = 80;
	int sock = connectToSocket(hostname, port);

	HttpRequest req = createHttpRequest("/");
	HttpResponse resp = getHttpResponse(sock, req);
	if (resp == NULL)
	{
		fprintf(stderr, "Error - doIt(): response is NULL\n");
		exit(EXIT_FAILURE);
	}
	printf("resp->statusCode=%d\n", resp->statusCode);
	printf("resp->statusMessage=%s\n", resp->statusMessage);
	printf("Content-Length: %d\n", resp->contentLength);
	puts("Content");
	puts("======================================");
	fwrite(resp->content, resp->contentLength, 1, stdout);
	fflush(stdout);

	freeHttpRequest(req);
	freeHttpResponse(resp);
}


int main (int argc, char* argv[])
{
	printf("Starting ...\n");
	doIt();
	printf("Done.\n");

	return 0;
}
