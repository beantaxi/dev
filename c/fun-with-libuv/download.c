#include <stdio.h>
#include <stdlib.h>
#include <uv.h>
#include "common.h"

char BIGBUFFER[1 << 20];
long nReadTotal = 0;
uv_buf_t downloadBuffer;
uv_tcp_t handle_tcp;
uv_connect_t req_connect;
uv_timer_t timer;
uv_fs_t req_fopen;
uv_fs_t req_write;
uv_fs_t req_close;
uv_file fd;

const char *PATH="/tmp/file.html";
/*
const char* request[] = 
{
"GET /content/cdr/contours/rtmLmp.png HTTP/1.1\r\n",
"Host: www.ercot.com\r\n",
"Accept: image/png\r\n",
"\r\n"
};
*/
const char* request[] = 
{
    "GET /~fdc/sample.html HTTP/1.1\r\n",
    "Host: www.columbia.edu\r\n",
    "Accept: text/html\r\n",
    "\r\n"
};

void onAlloc (uv_handle_t* handle, size_t suggestedSize, uv_buf_t* buf)
{
    *buf = downloadBuffer;
}

void onClose (uv_fs_t* req)
{
    fprintf(stderr, "onClose()!\n");
}


void onFileWrite (uv_fs_t* req)
{
    fprintf(stderr, "onFileWrite()");
    rc = uv_fs_close(&loop, &req_close, fd, onClose);
}

void onFileOpen (uv_fs_t* req)
{
    fprintf(stderr, "In onFileOpen (result=%ld)\n", req->result);
    if (req->result < 0)
    {
        printrc(req->result, "onFileOpen");
        exit(-1);
    }
    const char* body = (const char*)req->data;

    fd = (uv_file)req->result;
    fprintf(stderr, "fd=%d\n", fd);
    uv_buf_t buf = uv_buf_init((char*)body, strlen(body)+1);

    rc = uv_fs_write(&loop, &req_write, fd, &buf, 1, 0, onFileWrite);
    printrc(rc, "us_fv_write");
    
    fprintf(stderr, "Body\n");
    fprintf(stderr, "====\n");
//    fprintf(stderr, "%s", body);
}


void onRead (uv_stream_t* stream, ssize_t nread, const uv_buf_t* buf)
{
    fprintf(stderr, "onRead (nread=%ld nReadTotal=%ld)\n", nread, nReadTotal);
    
    if (nread < 0)
    {
        if (nread == UV_EOF)
        {
            uv_stop(&loop);
        }
    }
    else
    {
        memcpy(BIGBUFFER + nReadTotal, buf->base, nread);
        nReadTotal += nread;
    }
}

void processResponse ()
{
    long contentLength;

    char* last = BIGBUFFER;
    char* next;
    // Loop as long as you are getting lines delimited with \r\n. These are HTTP headers.
    while ((next = strstr(last, "\r\n")) != NULL)
    {
        long offset = next - last;
        fprintf(stderr, "substr found! offset=%ld\n", offset);
        char buf[offset+1];
        memset(buf, 0, sizeof(buf));
        strncpy(buf, last, offset);
        // Try and split the line on ': '. If you can, it's a valid header, and split it appropriately.   
        char* headerDelimiter = strstr(buf, ": ");
        if (headerDelimiter != NULL)
        {
            // name = everything up to the delimiter
            int nName = headerDelimiter - buf;
            char name[nName+1];
            memset(name, 0, sizeof(name));
            strncpy(name, buf, nName);
            // value = everything after the end of the delimiter
            int nValue = strlen(buf) - (nName + strlen(": ")); 
            char value[nValue + 1];
            memset(value, 0, sizeof(value));
            strncpy(value, headerDelimiter+strlen(": "), nValue);
            // echo the value
            fprintf(stderr, "%s: %s\n", name, value);
            if (strncasecmp(name, "content-length", strlen("content-length")) == 0)
            {
                contentLength = atoi(value);
            }
        }
        last = next + strlen("\r\n");
    }

    fprintf(stderr, "Content-Length=%ld\n", contentLength);
    char body[contentLength+1];
    memset(body, 0, sizeof(body));
    strncpy(body, last, contentLength);

    // Create a file and write to it
    req_fopen.data = strndup(body, strlen(body));
    req_fopen.cb = onFileOpen;
    rc = uv_fs_open(&loop, &req_fopen, PATH, UV_FS_O_TRUNC | UV_FS_O_CREAT, UV_FS_O_WRONLY, onFileOpen);
    printrc(rc, "uv_fs_open");
}


void onTimer (uv_timer_t* handle)
{
    fprintf(stderr, "Time!!!\n");
    processResponse();
    uv_stop(&loop);
}


void onWrite (uv_write_t* req, int status)
{
    // fprintf(stderr, "onWrite (%d buf(s))\n", req->nbufs);
    fprintf(stderr, "onWrite\n");
}

void onConnect (uv_connect_t* req, int status)
{
    fprintf(stderr, "Connected!\n");

    // Write the HTTP request

    int n = sizeof(request) / sizeof(request[0]);
    fprintf(stderr, "n=%d\n", n);
    for (int i=0; i<n; ++i)
    {
        uv_write_t* reqWrite = initWriteRequest(onWrite);
        uv_buf_t buf = uv_buf_init((char*)request[i], strlen(request[i]));
        rc = uv_write(reqWrite, req->handle, &buf, 1, reqWrite->cb);
        printrc(rc, "uv_write");
    }
    
    // Read the response
    int chunkSize = 1024;
    downloadBuffer = uv_buf_init(malloc(chunkSize), chunkSize);
    rc = uv_read_start(req->handle, onAlloc, onRead);
    printrc(rc, "uv_read_start");
}


void onHostnameResolution (uv_getaddrinfo_t* req, int status, struct addrinfo* data)
{
    printrc(status, "uv_getaddrinfo callback");
    if (status >= 0)
    {
        struct sockaddr* addr = data->ai_addr;
        switch (addr->sa_family)
        {
            case AF_INET:
            {
                fprintf(stderr, "IPv4!\n");
                struct sockaddr_in* addr_v4 = (struct sockaddr_in*)addr;
                char buf[addr_v4->sin_len];
                rc = uv_ip4_name(addr_v4, buf, sizeof(buf));
                printrc(rc, "uv_ip4_name");
                fprintf(stderr, "ip=%s!\n", buf);
                // *** Connect here! ***
                rc = uv_tcp_connect(&req_connect, &handle_tcp, addr, onConnect);
                printrc(rc, "uv_tcp_connect");
                break;
            }

            case AF_INET6:
            {
                fprintf(stderr, "IPv6!\n");
                // Cast the address to sockaddr_in6, and set up a char[], to receive the IP as a string
                struct sockaddr_in6* addr_v6 = (struct sockaddr_in6*)addr;
                char buf[addr_v6->sin6_len];
                rc = uv_ip6_name(addr_v6, buf, sizeof(buf));
                printrc(rc, "uv_ip6_name");
                fprintf(stderr, "ip=%s!\n", buf);
                // Init a TCP handle and connect to the ip addr
                rc = uv_tcp_connect(&req_connect, &handle_tcp, addr, onConnect);
                printrc(rc, "uv_tcp_connect");
                // Run the loop, to make the connection happen
                break;
            }

            default:
            {
                fprintf(stderr, "Unknown af_family (%d)!\n", addr->sa_family);
                break;
            }
        }
    }
    if (status >= 0)
    {
        uv_freeaddrinfo(data);
    }
    fprintf(stderr, "Leaving onHostnameResolution()\n");
    // Connect!
}


void onSigInt (uv_signal_t* handle, int signum)
{
    fprintf(stderr, "Ctrl-C!\n");
    processResponse();
    uv_stop(&loop);
}


int main ()
{
    memset(BIGBUFFER, 0, sizeof(BIGBUFFER));
    // Create event loop
    rc = uv_loop_init(&loop);
    printrc(rc, "uv_loop_init");

    // Set up a ctrl-c signal handler
    uv_signal_t sig;
    rc = uv_signal_init(&loop, &sig);
    printrc(rc, "uv_signal_init");
    rc = uv_signal_start_oneshot(&sig, onSigInt, SIGINT);
    printrc(rc, "uv_signal_start_oneshot");
    uv_unref((uv_handle_t*)&sig);
    
    
    // const char* hostName = "www.ercot.com";
    const char* hostName = "www.columbia.edu";
    const char* serviceName = "http";
    fprintf(stderr, "Resolving the hostname (%s / %s) ...\n", hostName, serviceName);
    struct addrinfo hints;
    memset(&hints, 0, sizeof(hints));
    hints.ai_family = PF_UNSPEC;
    hints.ai_socktype = SOCK_STREAM;
    uv_getaddrinfo_t req_addrInfo;
    rc = uv_getaddrinfo(&loop, &req_addrInfo, onHostnameResolution, hostName, serviceName, &hints);
    printrc(rc, "uv_getaddrinfo");
    rc = uv_tcp_init(&loop, &handle_tcp);
    printrc(rc, "uv_tcp_init");
    uv_unref((uv_handle_t*)&handle_tcp);

    rc = uv_timer_init(&loop, &timer);
    printrc(rc, "uv_timer");
    rc = uv_timer_start(&timer, onTimer, 10000, 0);
    printrc(rc, "uv_timer_start");
    
    fprintf(stderr, "About to run the loop ...\n");
    rc = uv_run(&loop, UV_RUN_DEFAULT);
    printrc(rc, "uv_run");
    
    fprintf(stderr, "Done!\n");

    // Stop & close the event loop
    uv_walk(&loop, on_walk_close_handle, (void*)NULL);
    rc = uv_run(&loop, UV_RUN_DEFAULT);
    printrc(rc, "uv_run");
    rc = uv_loop_close(&loop);
    printrc(rc, "uv_loop_close");
}