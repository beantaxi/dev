#include <stdlib.h>
#include "context.h"

Context* context_clone (Context* ctx)
{
    Context* ctx2 = malloc(sizeof(*ctx2));
    fprintf(stderr, "Created ctx2: %p\n", ctx2);
    memcpy(ctx2, ctx, sizeof(*ctx2));

    return ctx2;
}


void context_free (Context* ctx)
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
        bigBuffer_free(ctx->bb);
    }

    if (ctx->path != NULL)
    {
        free((void*)ctx->path);
    }
}


