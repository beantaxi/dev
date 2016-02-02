#include <errno.h>
#include <netdb.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>

void doIt ()
{
	int rc;
	const char* hostname = "euclid.ooc2000.com";
	char ipstr[INET6_ADDRSTRLEN];

	/* Step 1: Set up the address */
	struct addrinfo hint;
	memset(&hint, 0, sizeof(hint));
	hint.ai_family = AF_UNSPEC;
	hint.ai_socktype = SOCK_STREAM;
	const char* sPort = "80";
	struct addrinfo *pServiceInfo;
	rc = getaddrinfo(hostname, sPort, &hint, &pServiceInfo);
	if (rc != 0)
	{
		fprintf(stderr, "Error - getaddrinfo: %s\n", gai_strerror(rc));
		exit(1);
	}

	struct addrinfo* p;
	for (p = pServiceInfo; p != NULL; p=pServiceInfo->ai_next)
	{
		void* addr;
		printf("p->ai_family=%d\n", p->ai_family);
		if (p->ai_family == AF_INET)
		{
			struct sockaddr_in* ipv4 = (struct sockaddr_in*)p->ai_addr;
			addr = &(ipv4->sin_addr);
		}
		else if (p->ai_family == AF_INET6)
		{
			struct sockaddr_in6* ipv6 = (struct sockaddr_in6*)p->ai_addr;
			addr = &(ipv6->sin6_addr);
		}
		else
		{
			fprintf(stderr, "Unrecognized ai_family value: %d\n", p->ai_family);
		}
		inet_ntop(p->ai_family, addr, ipstr, sizeof(ipstr));
		printf("Address: %s\n", ipstr);
	}

	int s = socket(AF_INET, SOCK_STREAM, 0);
	if (s == -1)
	{
		perror("Error - socket()");
		exit(-1);
	}
	printf("s=%d\n", s);


	int addrlen;
	void* addr;
	p = pServiceInfo;
	addr = p->ai_addr;
	addrlen = p->ai_addrlen;
/*
	if (p->ai_family == AF_INET)
	{
		struct sockaddr_in* ipv4 = (struct sockaddr_in*)p->ai_addr;
		addr = &(ipv4->sin_addr);
		addrlen = sizeof(struct in_addr);
	}
	else if (p->ai_family == AF_INET6)
	{
		struct sockaddr_in6* ipv6 = (struct sockaddr_in6*)p->ai_addr;
		addr = &(ipv6->sin6_addr);
		addrlen = sizeof(struct in6_addr);
	}
	else
	{
		fprintf(stderr, "Error - ai_family: unrecognized value (%d)\n", addrlen);
	}
*/
	
	inet_ntop(p->ai_family, addr, ipstr, sizeof(ipstr));
	printf("addr=%s addrlen=%d\n", ipstr, addrlen);

	puts("Connecting ...");
	int thingee = connect(s, addr, addrlen);
	if (thingee == -1)
	{
		perror("Error - connect()");
		exit(1);
	}

	puts("Reading?!??? ....");
	char buf[1024];
	rc = read(s, buf, sizeof(buf));
	printf("%s\n", buf);

	


	free(pServiceInfo);


/*




	struct hostent* phe;
	phe = gethostbyname(url);
	if (phe == NULL)
	{
		fprintf(stderr, "Error - gethostbyname: %d", h_errno);
		exit(-1);
	}

	Print the address info
	printf("phe->h_name = %s\n", phe->h_name);
	int i = 0;
	while (phe->h_aliases[i] != NULL)
	{
		printf("phe->h_aliases[%d]=%s\n", i, phe->h_aliases[i]);
		++i;
	} 
	printf("phe->h_addrtype=%d\n", phe->h_addrtype);
	i = 0;
	printf("phe->h_addr_list=%p\n", phe->h_addr_list);
	while (phe->h_addr_list[i] != NULL)
	{
		puts("calling inet_ntoa() ...");
		char* sAddr = inet_ntoa(phe->h_addr_list[i]);
		printf("sAddr=%s\n", sAddr);
		puts("About to print stuff ...");
		printf("phe->h_addr_list[%d]=%s\n", i, sAddr);
		i++;
	}
*/
/*
	struct sockaddr_in addr;
	memset(&addr, 0, sizeof(addr));
	addr.sin_port = 80;
*/
}


int main (int argc, char* argv[])
{
	printf("Starting ...\n");
	doIt();
	printf("Done.\n");

	return 0;
}
