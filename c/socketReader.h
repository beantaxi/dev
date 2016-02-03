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

struct httpResponse
{
	int statusCode;
	char* statusMessage;
	char* content;
	int contentLength;
	HeaderNode headerList;
};
typedef struct httpResponse* HttpResponse;
