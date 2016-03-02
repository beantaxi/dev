#include <netdb.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/epoll.h>
#include "socketLib.h"

const int DEFAULT_TIMEOUT = 5000;

long getContentLength (HeaderNode headerList);
void handleResponse (int sock);
HeaderNode readHeaderList (int sock);
HttpResponseStatus readStatus (int sock);
const char* readUntil (int sock, const char* delim);
void streamResponse (int sock, long contentLength, FILE* outstream);


long getContentLength (HeaderNode headerList)
{
	return -1;
}


void handleResponse (int sock)
{
/*
	rc = recv(sock, buf, sizeof(buf), 0);
	if (rc == -1)
	{
		perror("Error - read()");
		exit(EXIT_FAILURE);
	}
*/
	HttpResponse resp = (HttpResponse)malloc(sizeof(struct httpResponse));
	resp->sock = sock;
	resp->status = readStatus(sock);
	resp->headerList = readHeaderList(sock);
	long contentLength = getContentLength(resp->headerList);
	
	printf("Status: %d %s\n", resp->status->code, resp->status->message);
	
	streamResponse(sock, contentLength, stdout);
	free(resp);
}


HeaderNode readHeaderList (int sock)
{
	return NULL;
}


HttpResponseStatus readStatus (int sock)
{
	const char* junk = readUntil(sock, " ");
	const char* sCode = readUntil(sock, " ");
	int code = atoi(sCode);
	free((void*)sCode);
	const char* message = readUntil(sock, "\r\n");

	HttpResponseStatus status = (HttpResponseStatus)malloc(sizeof(struct httpResponseStatus));
	status->code = code;
	status->message = message;

	return status;
}


void streamResponse (int sock, long contentLength, FILE* outstream)
{
}


int main (int argc, char* argv[])
{
	int rc;

	int timeout;
	if (argc > 1)
	{
		timeout = atoi(argv[1]);
	}
	else
	{
		timeout = DEFAULT_TIMEOUT;
	}

	const char* hostname = "euclid.ooc2000.com";
	int port = 80;

	AddrInfo addressList = createAddressInfoList(hostname, port);
	char sPort[10];
	snprintf(sPort, sizeof(sPort), "%d", port);

	int sock;
	AddrInfo p;
	for (p = addressList; p != NULL; p->ai_next)
	{
		sock = socket(p->ai_family, p->ai_socktype | SOCK_NONBLOCK, 0);
		if (sock != -1)
		{
			break;
		}
	}

	int epfd = epoll_create1(0);
	if (epfd == -1)
	{
		perror("Error - epoll_create1");
		exit(EXIT_FAILURE);
	}
	struct epoll_event epEventTemplate;
//	epEvent.events = EPOLLIN | EPOLLRDHUP;
	epEventTemplate.events = EPOLLOUT | EPOLLRDHUP | EPOLLHUP;
	memset(&epEventTemplate.data, 0, sizeof(epEventTemplate.data));
	rc = epoll_ctl(epfd, EPOLL_CTL_ADD, sock, &epEventTemplate);
	if (rc == -1)
	{
		perror("Error - epoll_ctl()");
		exit(EXIT_FAILURE);
	}

	/** Connect to the socket */
	rc = connect(sock, p->ai_addr, p->ai_addrlen);
	if (rc != -1)
	{
		perror("Error - connect()");
		exit(EXIT_FAILURE);
	}
	freeaddrinfo(addressList);

	/** Wait for the connection to be ready to write */
	printf("Waiting to write (timeout=%d ms) ...\n", timeout);
	struct epoll_event epEvent;
	rc = epoll_wait(epfd, &epEvent, sizeof(epEvent), timeout);
	if (rc == -1)
	{
		perror("Error - epoll_wait()");
		exit(EXIT_FAILURE);
	}
	printf("rc=%d\n", rc);
	if (rc == 0)
	{
		fputs("Timed out waiting for a connection.\n", stdout);
		exit(EXIT_FAILURE);
	}
	
	bool isReadyToWrite = false;
	printf("epEvent.events=%d\n", epEvent.events);
	if (epEvent.events & EPOLLOUT)
	{
		puts("Ready for writing!");
		isReadyToWrite = true;
	}
	if (epEvent.events & EPOLLHUP)
	{
		puts("Got EPOLLHUP. Hope that makes sense.");
	}
	if (epEvent.events & !(EPOLLOUT | EPOLLHUP))
	{
		printf("??? Event code = %d\n", epEvent.events);
	}
	

	char buf[100000];
	if (isReadyToWrite)
	{
		const char* requestString = createHttpRequestString("/");
		printf("requestString=%s\n", requestString);
		sprintf(buf, "%s%s", requestString, "\r\n");
		free((void*)requestString);
		printf("strlen(buf)=%ld\n", strlen(buf));
		fflush(stdin);
		rc = send(sock, buf, strlen(buf), MSG_DONTWAIT);
		if (rc == -1)
		{
			perror("Error - send");
			exit(EXIT_FAILURE);
		}
		printf("%d byte(s) written\n", rc);
	}


/*
	rc = epoll_ctl(epfd, EPOLL_CTL_DEL, sock, NULL);
	if (rc == -1)
	{
		perror("Error - epoll_ctl()");
		exit(EXIT_FAILURE);
	}
	epEventTemplate.events = EPOLLIN | EPOLLPRI;
	memset(&epEventTemplate.data, 0, sizeof(epEventTemplate.data));
	puts("Switching to read mode ...");
	rc = epoll_ctl(epfd, EPOLL_CTL_ADD, sock, &epEventTemplate);
	if (rc == -1)
	{
		perror("Error - epoll_ctl()");
		exit(EXIT_FAILURE);
	}
*/


	epEventTemplate.events = EPOLLIN | EPOLLPRI;
	printf("epEventTemplate.events=%d\n", epEventTemplate.events);
	memset(&epEventTemplate.data, 0, sizeof(epEventTemplate.data));
	puts("Switching to read mode ...");
	rc = epoll_ctl(epfd, EPOLL_CTL_MOD, sock, &epEventTemplate);
	if (rc == -1)
	{
		perror("Error - epoll_ctl()");
		exit(EXIT_FAILURE);
	}

	bool isReadyToRead = false;
	puts("Waiting for data to read ...");
	rc = epoll_wait(epfd, &epEvent, 1, timeout);
	if (rc == -1)
	{
		perror("Error - epoll_wait()");
		exit(EXIT_FAILURE);
	}
	printf("rc=%d\n", rc);
	if (rc == 0)
	{
		puts("Timed out waiting to read");
		exit(EXIT_FAILURE);
	}
	printf("epEvent.events=%d\n", epEvent.events);
	if (epEvent.events & EPOLLIN)
	{
		puts("Ready to read!");
		isReadyToRead = true;
	}
	if (epEvent.events & EPOLLPRI)
	{
		puts("Got a EPOLLPRI. Weird?");
		isReadyToRead = true;
	}
	if (epEvent.events & EPOLLHUP)
	{
		puts("Got EPOLLUP. Hope that makes sense.");
	}

	if (isReadyToRead)
	{
		// LAME but this is how I'm reading for now
		handleResponse(sock);
	}

	puts("Done.");

	return EXIT_SUCCESS;
}


