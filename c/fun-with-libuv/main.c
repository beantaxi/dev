#include <assert.h>
#include <stdlib.h>
#include <uv.h>
#include "bigBuffer.h"
#include "common.h"
#include "string.h"

typedef struct Context_s
{
    struct addrinfo* addrInfo;
    uv_tcp_t* tcpHandle;
    BigBuffer* bb;
} Context;

void connectToHost (Context* ctx);
Context* cloneContext (Context* ctx);
void dumpAddresses (struct addrinfo* addInfo);
void freeHandle (uv_handle_t* handle);
void sendHttpRequest (Context* ctx, uv_connect_t* req);

void onAsync (uv_async_t* handle);
void onHostnameResolution (uv_getaddrinfo_t* reqi, int status, struct addrinfo* addrInfo);
void onConnect (uv_connect_t* req, int status);
void onHttpSend (uv_write_t* req, int status);
void onHttpRecv (uv_stream_t* stream, ssize_t nRead, const uv_buf_t* buf);
void onFileOpen (uv_fs_t* req);
void onFileWrite (uv_fs_t* req);
void onFileClose (uv_fs_t* req);

const char* request[] = 
{
"GET /content/cdr/contours/rtmLmp.png HTTP/1.1\r\n",
"Host: www.ercot.com\r\n",
"Accept: image/png\r\n",
"\r\n"
};

Context* cloneContext (Context* ctx)
{
    Context* ctx2 = malloc(sizeof(*ctx2));
    fprintf(stderr, "Created ctx2: %p\n", ctx2);
    memcpy(ctx2, ctx, sizeof(*ctx2));

    return ctx2;
}


/*
    Context
        Assumes: ctx->addrInfo->ai_addr != NULL
        Sets:    ctx->tcpHandle = empty handle (uv_tcp_t)
    Request
        Sets:    req_connect->data = ctx
*/
void connectToHost (Context* ctx)
{
    assert(ctx != NULL);
    assert(ctx->addrInfo != NULL);
    assert(ctx->addrInfo->ai_addr != NULL);

    // Connect
    ctx->tcpHandle = malloc(sizeof(uv_tcp_t));
    fprintf(stderr, "Created ctx->tcpHandle: %p\n", ctx->tcpHandle);
    memset(ctx->tcpHandle, 0, sizeof(uv_tcp_t));
    rc = uv_tcp_init(&loop, ctx->tcpHandle);
    printrc(rc, "uv_tcp_init");

    uv_connect_t* req_connect = malloc(sizeof(uv_connect_t));
    fprintf(stderr, "Created req_connect: %p\n", req_connect);
    memset(req_connect, 0, sizeof(uv_connect_t));
    req_connect->data = ctx;
    rc = uv_tcp_connect(req_connect, ctx->tcpHandle, ctx->addrInfo->ai_addr, onConnect);
    printrc(rc, "uv_tcp_connect");
}


void dumpAddresses (struct addrinfo* addrInfo)
{
    struct addrinfo* curr;
    char buf[UV_IF_NAMESIZE+1];
    fprintf(stderr, "addresses\n");
    for (curr = addrInfo; curr != NULL; curr = curr->ai_next)
    {
//        rc = uv_inet_ntop(curr->ai_family, curr->ai_addr, buf, sizeof(buf));
//        printrc(rc, "uv_inet_ntop");
        rc = uv_ip4_name((struct sockaddr_in*)addrInfo->ai_addr, buf, sizeof(buf));
        printrc(rc, "uv_ip4_name");
        if (rc >= 0)
        {
            fprintf(stderr, "ip=%s\n", buf);
        }
    }
}


void freeBigBuffer (BigBuffer* bb)
{
    if (bb->data != NULL)
    {
        free(bb->data);
    }

    free(bb);
}


void freeContext (Context* ctx)
{
    if (ctx->addrInfo != NULL)
    {
        uv_freeaddrinfo(ctx->addrInfo);
    }

    if (ctx->tcpHandle != NULL)
    {
        if (ctx->tcpHandle->data != NULL)
        {
            free(ctx->tcpHandle->data);
        }
        free(ctx->tcpHandle);
    }

    if (ctx->bb != NULL)
    {
        freeBigBuffer(ctx->bb);
    }
}


/*
    Request
        Sets:   req_write->data = ctx
*/
void sendHttpRequest (Context* ctx, uv_connect_t* req)
{
    // Write the http request
    int nLines = sizeof(request) / sizeof(request[0]);
    uv_buf_t bufs[nLines];
    for (int i=0; i<nLines; ++i)
    {
        const char* s = strdup(request[i]);
        bufs[i] = uv_buf_init((char*)s, strlen(s));
    }
    uv_write_t* req_write = malloc(sizeof(uv_write_t));
    fprintf(stderr, "Created req_write: %p\n", req_write);
    memset(req_write, 0, sizeof(*req_write));
    req_write->data = ctx;
    rc = uv_write(req_write, req->handle, bufs, sizeof(bufs)/sizeof(bufs[0]), onHttpSend);
    printrc(rc, "uv_write");
}


/******************************************************************************
 * 
 * Callbacks
 * 
 ******************************************************************************/

void onAlloc (uv_handle_t* handle, size_t suggestedSize, uv_buf_t* buf)
{
    buf->base = malloc(suggestedSize);
    fprintf(stderr, "Created buf->base: %p\n", buf->base);
    memset(buf->base, 0, suggestedSize);
    buf->len = suggestedSize;
}


void onAsync (uv_async_t* handle)
{
    fprintf(stderr, "onAsync()\n");
    uv_close((uv_handle_t*)handle, on_close);
}


/*
    Context
        Requires:   ctx->addrInfo != NULL
                    ctx->tcpHandle != NULL
    Actions
        Calls:      sendHttpRequest()
*/
void onConnect (uv_connect_t* req, int status)
{
    fprintf(stderr, "onConnect(): status=%d req->data=%p\n", status, req->data);
    Context* ctx = (Context*)req->data;
    assert(ctx != NULL);
    assert(ctx->addrInfo != NULL);
    assert(ctx->tcpHandle != NULL);

    sendHttpRequest(ctx, req); 
    
    free(req);
}


void onFileClose (uv_fs_t* req)
{
    // Free up file resources if necessary
}


void onFileOpen (uv_fs_t* req)
{
    // Write the file
}


void onFileWrite (uv_fs_t* req)
{
    // Free up read buffers
    // Close the file
}


/*
    Context
        Requires: ctx != null
        Sets:     ctx->addrInfo = addrInfo
*/
void onHostnameResolution (uv_getaddrinfo_t* req, int status, struct addrinfo* addrInfo)
{
    fprintf(stderr, "onHostnameResolution(): status=%d %s %s\n", status, uv_err_name(status), uv_strerror(status));
    if (status == UV_EAI_NONAME)
    {
        fprintf(stderr, "Please confirm you have an Internet connection\n");
        exit(status);
    }
    // Get the context, assert it's been set, & add the addrInfo
    Context* ctx = (Context*)req->data;
    assert(ctx != NULL);
    ctx->addrInfo = addrInfo;

    dumpAddresses(addrInfo);
    // Connect
    connectToHost(ctx);

    free(req);
}


void onHttpRecv (uv_stream_t* stream, ssize_t nRead, const uv_buf_t* buf)
{
    assert(stream->data != NULL);

    fprintf(stderr, "onHttpRecv: nRead=%ld buf->len=%ld\n", nRead, buf->len);
    if (nRead == UV_EOF)
    {
        fprintf(stderr, "EOF reached!");
    }
    else
    {
        Context* ctx = (Context*)stream->data;
        bigBuffer_append(ctx->bb, buf->base, nRead);
    }
}


void onHttpSend (uv_write_t* req, int status)
{
    fprintf(stderr, "onHttpSend(): status=%d req->data=%p\n", status, req->data);
    // Start a reader on the TCP stream

    assert(req->data != NULL);
    assert(req->handle != NULL);
    uv_stream_t* stream = req->handle;
    stream->data = cloneContext((Context*)req->data);
    rc = uv_read_start(stream, onAlloc, onHttpRecv);
    printrc(rc, "uv_read_start");

    free(req);
}


void onTimer (uv_timer_t* handle)
{
    fprintf(stderr, "onTimer(): flags=%d\n", handle->flags);

    assert(handle->data != NULL);
    Context* ctx = (Context*)handle->data;
    assert(ctx->tcpHandle != NULL);

    fprintf(stderr, "Timer is up. ctx->bb->size=%ld\n", ctx->bb->size);

    uv_close((uv_handle_t*)ctx->tcpHandle, on_close);   

    // I honestly don't know why this async stuff is here. Maybe I was just playing.
    uv_async_t* handle_async = malloc(sizeof(uv_async_t));
    fprintf(stderr, "Created handle_async: %p\n", handle_async);
    memset(handle_async, 0, sizeof(*handle_async));
    rc = uv_async_init(&loop, handle_async, onAsync);
    printrc(rc, "uv_async_init");
    uv_unref((uv_handle_t*)handle_async);
    rc = uv_async_send(handle_async);
    printrc(rc, "uv_async_send");
}


int main ()
{
    // Create event loop
    rc = uv_loop_init(&loop);
    //printrc(rc, "uv_loop_init");

    Context* ctx = malloc(sizeof(Context));
    fprintf(stderr, "Created ctx: %p\n", ctx);
    ctx->bb = bigBuffer_create(0);

    // Set up the timer
    uv_timer_t* handle_timer = malloc(sizeof(uv_timer_t));
    fprintf(stderr, "Created handle_timer: %p\n", handle_timer);
    memset(handle_timer, 0, sizeof(*handle_timer));
    handle_timer->data = ctx;
    rc = uv_timer_init(&loop, handle_timer);
    printrc(rc, "uv_timer_init");
    rc = uv_timer_start(handle_timer, onTimer, 10000, 10000);
    uv_unref((uv_handle_t*)handle_timer);

    // Lookup the hostname
    const char* hostName = "www.ercot.com";
    const char* serviceName = "http";
    struct addrinfo hints = {};
    hints.ai_socktype = SOCK_STREAM;
    hints.ai_protocol = IPPROTO_TCP;
    uv_getaddrinfo_t* req_getAddrInfo = malloc(sizeof(uv_getaddrinfo_t));
    fprintf(stderr, "Created req_getAddrInfo: %p\n", req_getAddrInfo);
    req_getAddrInfo->data = ctx;

    rc = uv_getaddrinfo(&loop, req_getAddrInfo, onHostnameResolution, hostName, serviceName, &hints);
    printrc(rc, "uv_getaddrinfo");

    rc = uv_run(&loop, UV_RUN_DEFAULT);
    printrc(rc, "uv_run");

    // Stop & close the event loop
    uv_walk(&loop, on_walk_close_handle, (void*)NULL);
    rc = uv_run(&loop, UV_RUN_DEFAULT);
    printrc(rc, "uv_run");
    rc = uv_loop_close(&loop);
    printrc(rc, "uv_loop_close");
}    