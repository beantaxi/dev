#include <errno.h>
#include <netdb.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <sys/socket.h>
#include <sys/types.h>
#include "socketReader.h"

AddrInfo createAddrInfos (const char* hostname, int port)
{
	int rc;

	// Set up hint
	AddrInfo hints = (AddrInfo)malloc(sizeof(struct addrinfo));
	memset(hints, 0, sizeof(struct addrinfo));
	hints->ai_family = AF_UNSPEC;
	hints->ai_socktype = SOCK_STREAM;
	char sPort[10];
	rc = snprintf(sPort, sizeof(sPort), "%d", port);
	if (rc > sizeof(sPort))
	{
		fprintf(stderr, "Error - createAddrInfo(): invalid port value (%d); too big\n", port);
		exit(EXIT_FAILURE);
	}
	
	AddrInfo pResults;
	rc = getaddrinfo(hostname, sPort, hints, &pResults);
	if (rc != 0)
	{
		fprintf(stderr, "Error - getaddrinfo(): %s\n", gai_strerror(rc));
		exit(EXIT_FAILURE);
	}
	free(hints);

	return pResults;
}


int connectToSocket (AddrInfo pServiceInfos)
{
	int sock;

	AddrInfo p;
	for (p = pServiceInfos; p != NULL; p = p->ai_next)
	{
		sock = socket(p->ai_family, p->ai_socktype, p->ai_protocol); 
		if (sock == -1)
		{
			continue;
		}
		if (connect(sock, p->ai_addr, p->ai_addrlen) == -1)
		{
			perror("Warning - connect()");
			close(sock);
			continue;
		}
		break;
	}

	if (p == NULL)
	{
		fprintf(stderr, "Error - connectToSocket(): No valid address found.\n");
		exit(EXIT_FAILURE);
	}
	
	return sock;
}

HttpRequest createHttpRequest (const char* path)
{
	HttpRequest req = (HttpRequest)malloc(sizeof(struct httpRequest));
	req->path = strdup(path);
	req->headerList = NULL;
	
	return req;
}


HttpRequest addHeader (HttpRequest req, char* name, char* value)
{
	HeaderNode node = (HeaderNode)malloc(sizeof(struct headerNode));
	struct httpHeader header;
	node->header.name = name;
	node->header.value = value;
	node->next = NULL;

	if (req->headerList == NULL)
	{
		req->headerList = node;
	}
	else
	{
		HeaderNode curr;
		for (curr = req->headerList; curr->next != NULL; curr=curr->next)
			;
		curr->next = node;
	}

	return req;
}


HttpResponse addResponseHeader (HttpResponse resp, char* name, char* value)
{
	HeaderNode node = (HeaderNode)malloc(sizeof(struct headerNode));
	struct httpHeader header;
	node->header.name = name;
	node->header.value = value;
	node->next = NULL;

	if (resp->headerList == NULL)
	{
		resp->headerList = node;
	}
	else
	{
		HeaderNode curr;
		for (curr = resp->headerList; curr->next != NULL; curr=curr->next)
			;
		curr->next = node;
	}

	return resp;
}


void freeHttpRequest (HttpRequest req)
{
	free((void*)req->path);
	HeaderNode last, curr;
	curr = req->headerList;
	while (curr != NULL)
	{
		free((void*)curr->header.name);
		free((void*)curr->header.value);
		last = curr;
		curr = curr->next;
		free(last);
	}

	free(req);
}


void freeHttpResponse (HttpResponse resp)
{
	free((void*)resp->statusMessage);
	free((void*)resp->content);
	HeaderNode last, curr;
	curr = resp->headerList;
	while (curr != NULL)
	{
		free((void*)curr->header.name);
		free((void*)curr->header.value);
		last = curr;
		curr = curr->next;
		free(last);
	}

	free(resp);
}



HttpResponse getHttpResponse (int sock, HttpRequest req)
{
	const char* const eot = "\r\n";
	char buf[100000];
	sprintf(buf, "GET %s HTTP/1.0\r\n", req->path);
	write(sock, buf, strlen(buf));
	write(sock, eot, strlen(eot));

	HttpResponse resp = (HttpResponse)malloc(sizeof(struct httpResponse));
	memset(resp, 0, sizeof(struct httpResponse));
	
	// Inhale the whole thing
	int nRead = read(sock, buf, sizeof(buf));
	
	// Get the first line
	const char* eol = "\r\n";
	char* delim = " ";
	char* curr = buf;
	int n;
	// Skip first token (HTTP/1.0)
	n = strcspn(curr, delim);
	curr += n+1;
	// Get status code (eg 200)
	n = strcspn(curr, delim);
	char* sStatusCode = strndup(curr, n);
	resp->statusCode = atoi(sStatusCode);
	free(sStatusCode);
	curr += n+1;
	// Get status message (eg "OK")
	n = strcspn(curr, eol);
	resp->statusMessage = strndup(curr, n);
	curr += n+strlen(eol);

	// Loop over header lines, until first blank line
	char line[1024];
	char* end;
	char* token = ": ";
	char* sToken;
	while ((end = strstr(curr, eol)) != curr)
	{
		strncpy(line, curr, end-curr);
		line[end-curr] = '\0';
		sToken = strstr(line, token);
		char* name = strndup(line, sToken-line);
		printf("name=%s\n", name);
		char* value = strndup(sToken+2, strlen(line)-(sToken-line)+2);
		printf("value=%s\n", value);
		addResponseHeader(resp, name, value);
		curr = end+strlen(eol);
	}
	curr += strlen(eol);
	
	// Calc content length, and set content & content length
	int offset = curr - buf;
	int nLeft = nRead - offset;
	resp->content = strndup(curr, nLeft);
	resp->contentLength = nLeft;
	
	return resp;
}


const char* getIpAddress (AddrInfo ai, char* s, int n)
{
	void* addr;
	if (ai->ai_family == AF_INET)
	{
		struct sockaddr_in* ipv4 = (struct sockaddr_in*)ai->ai_addr;
		addr = &(ipv4->sin_addr);
	}
	else if (ai->ai_family == AF_INET6)
	{
		struct sockaddr_in6* ipv6 = (struct sockaddr_in6*)ai->ai_addr;
		addr = &(ipv6->sin6_addr);
	}
	else
	{
		fprintf(stderr, "Unrecognized ai_family value: %d\n", ai->ai_family);
		exit(EXIT_FAILURE);
	}

	const char* r = inet_ntop(ai->ai_family, addr, s, n);
	return r;
}


void doIt ()
{
	int rc;
	const char* const hostname = "euclid.ooc2000.com";
	char const ipstr[INET6_ADDRSTRLEN];

	int port = 80;
	AddrInfo pServiceInfos = createAddrInfos(hostname, port);
	int sock = connectToSocket(pServiceInfos);
	freeaddrinfo(pServiceInfos);

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
//	puts(resp->content);
	fflush(stdout);

	freeHttpRequest(req);
	freeHttpResponse(resp);

/*
	puts("Writing?!?!? ...");
	const char* const request = "GET / HTTP/1.0\r\n\r\n";
	write(sock, request, strlen(request));

	puts("Reading?!?!? ....");
	char buf[1024];
	rc = read(sock, buf, sizeof(buf));
	printf("%s\n", buf);
*/
}


int main (int argc, char* argv[])
{
	printf("Starting ...\n");
	doIt();
	printf("Done.\n");

	return 0;
}
