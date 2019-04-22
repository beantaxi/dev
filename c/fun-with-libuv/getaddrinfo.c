#include <arpa/inet.h>
#include <netdb.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <sys/types.h>

typedef struct ip_s
{
    const struct addrinfo* addr;
    const char* s;
    const char* (*toString) (const struct ip_s* ip);
} ip_t;


const char* toStringIp4 (const ip_t* ip)
{
    char buf[INET6_ADDRSTRLEN];
    char buf2[sizeof(buf)+20];
    const char* dummy = inet_ntop(ip->addr->ai_family, &((const struct sockaddr_in*)ip->addr->ai_addr)->sin_addr, buf, sizeof(buf));
    sprintf(buf2, "IP4: %s", buf);

    const char* dup = strdup(buf2);

    return dup;
}


const char* toStringIp6 (const ip_t* ip)
{
    char buf[INET6_ADDRSTRLEN];
    char buf2[sizeof(buf)+20];
    const char* dummy = inet_ntop(ip->addr->ai_family, &((const struct sockaddr_in6*)ip->addr->ai_addr)->sin6_addr, buf, sizeof(buf));
    sprintf(buf2, "IP6: %s", buf);

    const char* dup = strdup(buf2);

    return dup;
}



ip_t* createIp (const struct addrinfo* addr)
{
    ip_t* ip = (ip_t*)malloc(sizeof(ip_t));
    ip->addr = addr;
    char s[INET6_ADDRSTRLEN];
    switch (addr->ai_addr->sa_family)
    {
        case AF_INET: ip->s = toStringIp4(ip); break;
        case AF_INET6: ip->s = toStringIp6(ip); break;
        /*
        {
            const char* dummy = inet_ntop(addr->ai_family, &((const struct sockaddr_in*)addr->ai_addr)->sin_addr, s, sizeof(s));
            ip->s = strndup(s, sizeof(s));
            break;
        }
        */
        /*
        case AF_INET6: 
        {
            const char* dummy = inet_ntop(addr->ai_family, &((const struct sockaddr_in6*)addr->ai_addr)->sin6_addr, s, sizeof(s));
            ip->s = strndup(s, sizeof(s));
            break;
        }
        */
        default: printf("Unknown sa_family\n"); break;
    }

    return ip;

}

/*
void printAddress (const struct addrinfo* addr)
{
    printf("ai->next=%p\n", addr->ai_next);
    printf("sa_family=%d\n", addr->ai_addr->sa_family);
    ip_t* ip = createIp(addr);

    switch (addr->ai_addr->sa_family)
    {
        case AF_INET:
        {
            printf("IPv4: %s\n", ip->s);
            break;
        }
        case AF_INET6: 
        {
            printf("IPv6: %s\n", ip->s);
            break;
        }
        default: printf("Unknown sa_family\n"); break;
    }
}
*/


int main ()
{
    printf("getaddrinfo!\n");
    struct addrinfo* addr;
    struct addrinfo hints = {};
    hints.ai_socktype = SOCK_STREAM;
    hints.ai_protocol = IPPROTO_TCP;
    const char* hostname = "www.ercot.com";
//    const char* hostname = "www.rabobank.nl";
    const char* serviceName = "https";

    int rc = getaddrinfo(hostname, serviceName, &hints, &addr);
    if (rc < 0)
    {
        fprintf(stderr, "rc=%d\n", rc);
        exit(rc);
    } 
    
    struct addrinfo* curr;
    for (curr = addr; curr != NULL; curr = curr->ai_next)
    {
        ip_t* ip = createIp(curr);
        printf("%s\n", ip->s);
    }

    freeaddrinfo(addr);
}