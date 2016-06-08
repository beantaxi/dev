#include "socketLib.h"
#include <errno.h>
#include <netdb.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <sys/types.h>

int checkAllAddressesForConnection (AddrInfo addressList);
AddrInfo createHints ();


HttpRequest addRequestHeader (HttpRequest req, char* name, char* value)
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


int connectToSocket (const char* hostname, int port)
{
	AddrInfo addressInfoList = createAddressInfoList(hostname, port);
	int sock = checkAllAddressesForConnection(addressInfoList);
	freeaddrinfo(addressInfoList);
	
	return sock;
}


/*
int connectToSocket (AddrInfo pServiceInfos)
{
	int sock;

	AddrInfo hints = createHints();
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

	sock = 

	if (p == NULL)
	{
		fprintf(stderr, "Error - connectToSocket(): No valid address found.\n");
		exit(EXIT_FAILURE);
	}
	
	return sock;
}
*/

AddrInfo createAddressInfoList (const char* hostname, int port)
{	
	int rc;

	AddrInfo hints = createHints();
	char sPort[10];
	snprintf(sPort, sizeof(sPort), "%d", port);
	AddrInfo addressInfoList;
	rc = getaddrinfo(hostname, sPort, hints, &addressInfoList);
	free(hints);
	if (rc != 0)
	{
		fprintf(stderr, "Error - getaddrinfo(): %s\n", gai_strerror(rc));
		exit(EXIT_FAILURE);
	}

	return addressInfoList;
}


HttpRequest createHttpRequest (const char* path)
{
	HttpRequest req = (HttpRequest)malloc(sizeof(struct httpRequest));
	req->path = strdup(path);
	req->headerList = NULL;
	
	return req;
}

const char* createHttpRequestString (const char* path)
{
	const char* const eot = "\r\n";
	char buf[100000];
	sprintf(buf, "GET %s HTTP/1.0\r\n", path);
	char* requestString = (char*)malloc(strlen(buf)+1);
	strncpy(requestString, buf, strlen(buf)+1);
	return requestString;
}

AddrInfo createHints ()
{
	AddrInfo hints = (AddrInfo)malloc(sizeof(struct addrinfo));
	memset(hints, 0, sizeof(struct addrinfo));
	hints->ai_family = AF_UNSPEC;
	hints->ai_socktype = SOCK_STREAM;

	return hints;
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
	free((void*)resp->status->message);
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
	resp->status->code = atoi(sStatusCode);
	free(sStatusCode);
	curr += n+1;
	// Get status message (eg "OK")
	n = strcspn(curr, eol);
	resp->status->message = strndup(curr, n);
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


int readChar (int fd)
{
	char c;
	int rc = read(fd, &c, 1);
	if (rc == -1)
	{
		perror("Error - readChar");
		exit(EXIT_FAILURE);
	}
	// Check for EOF
	if (rc == 0)
	{
		c = -1;
	}

	return c;
}


const char* readUntil (int fd, const char* delim)
{
	int rc;
	bool done = false;
	int nRead = 0;
	int c;
	char* s = NULL;
	while (!done)
	{
		
		c = readChar(fd);
		// If we hit EOF before we find delim, we're done.
		if (c == -1)
		{
			break;
		}
		// If we find the first character of the delim, we need to see if we've found delim
		if (c == delim[0])
		{
			bool isDelim = true;
			char* possibleDelim = (char*)malloc(1);
			possibleDelim[0] = c;
			// Keep reading until strlen(delim), or until you miss. 
			// (i=1 cause we already have the first character)
			int nDelim;
			for (nDelim=1; nDelim<strlen(delim); ++nDelim)
			{
				c = readChar(fd);
				if (c == -1)
				{
					goto end;
				}
				possibleDelim[nDelim] = c;
				// If c doesn't match we don't have the delim.
				if (c != delim[nDelim])
				{
					break;
				}
			}
			// If we did not find the delim, we need to copy all the characters we've found to
			// the string we've read. Otherwise we're done.
			if (!isDelim)
			{
				strncpy(s+nRead, possibleDelim, nDelim);
				nRead += nDelim;
			}
			else
			{
				done = true;
				break;
			}
		}
		else
		{
			nRead++;
			s = realloc(s, nRead);
			s[nRead-1] = c;
		}
	}

	end:
	if (!done)
	{
		if (s != NULL)
		{
			free(s);
			s = NULL;
		}
	}

	return s;
}



/*
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


HttpRequest createHttpRequest (const char* path)
{
	HttpRequest req = (HttpRequest)malloc(sizeof(struct httpRequest));
	req->path = strdup(path);
	req->headerList = NULL;
	
	return req;
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
*/

int checkAllAddressesForConnection (AddrInfo addressList)
{
	int sock = -1;

	AddrInfo p;
	for (p = addressList; p != NULL; p = p->ai_next)
	{
		// First - create the socket and check if the creation failed
		sock = socket(p->ai_family, p->ai_socktype, p->ai_protocol); 
		if (sock == -1)
		{
			perror("Warning - socket()");
			continue;
		}
		// Second - try and connect to the current address, and check if the connection failed
		if (connect(sock, p->ai_addr, p->ai_addrlen) == -1)
		{
			perror("Warning - connect()");
			close(sock);
			sock = -1;
			continue;
		}
		// If we made it this far, then we found a valid socket. So we're done.
		break;
	}

	if (sock == -1)
	{
		fprintf(stderr, "Error - connectToSocket(): No valid address found.\n");
		freeaddrinfo(addressList);
		exit(EXIT_FAILURE);
	}
	
	return sock;
}
