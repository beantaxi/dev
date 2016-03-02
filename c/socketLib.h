#include <stdio.h>
#include <sys/socket.h>

typedef struct addrinfo* AddrInfo;
typedef struct sockaddr* SockAddr;

struct httpHeader
{
	const char* name;
	const char* value;
};

struct headerNode
{
	struct httpHeader header;
	struct headerNode* next;
};
typedef struct headerNode* HeaderNode;

struct httpRequest
{
	const char* path;
	HeaderNode headerList;
};
typedef struct httpRequest* HttpRequest;

struct httpResponseStatus
{
	int code;
	const char* message;
};
typedef struct httpResponseStatus* HttpResponseStatus;

struct httpResponse
{
	int sock;
	struct httpResponseStatus* status;
	HeaderNode headerList;
};
typedef struct httpResponse* HttpResponse;

HttpRequest addRequestHeader (HttpRequest req, char* name, char* value);
HttpResponse addResponseHeader (HttpResponse resp, char* name, char* value);
int connectToSocket (const char* hostname, int port);
AddrInfo createAddressInfoList (const char* hostname, int port);
HttpRequest createHttpRequest (const char* path);
const char* createHttpRequestString (const char* path);
void freeHttpRequest (HttpRequest req);
void freeHttpResponse (HttpResponse resp);
HttpResponse getHttpResponse (int sock, HttpRequest req);
const char* getIpAddress (AddrInfo ai, char* s, int n);
const char* readUntil (int fdIn, const char* delim);

