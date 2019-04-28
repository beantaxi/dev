#include <uv.h>
#include "bigBuffer.h"

typedef struct Context_s
{
    struct addrinfo* addrInfo;
    uv_tcp_t* tcpHandle;
    BigBuffer* bb;
    const char* path;
} Context;

Context* context_clone (Context* ctx);
void context_free (Context* ctx);