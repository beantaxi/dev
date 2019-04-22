#include <stdio.h>
#include <stdlib.h>
#include "common.h"

int rc = 0;
uv_loop_t loop = {};
my_loop_t myloop = {};
uv_pipe_t pipe_stdin = {};
uv_pipe_t pipe_stdout = {};
uv_pipe_t pipe_stderr = {};


int init_stdout ()
{
    rc = uv_pipe_init(&loop, &pipe_stdout, 0);
    printrc(rc, "uv_pipe_init");

    return rc;
}


/*
uv_write_t* initReadRequest (uv_write_cb cb)
{
    uv_write_t* req = (uv_write_t*)malloc(sizeof(uv_write_t));
    req->cb = cb;

    return req;
}
*/

uv_write_t* initWriteRequest (uv_write_cb cb)
{
    uv_write_t* req = (uv_write_t*)malloc(sizeof(uv_write_t));
    req->cb = cb;

    return req;
}


void on_alloc (uv_handle_t* handle, size_t size, uv_buf_t* buf)
{
    printf("In on_alloc(): size=%ld\n", size);
    buf->len = size;
    buf->base = malloc(buf->len);
}


void on_close (uv_handle_t* handle)
{
    fprintf(stderr, "Inside on_close(): %p ...\n", handle);

    if (handle->data != NULL)
    {
        fprintf(stderr, "Freeing handle->data: %p ...\n", handle->data);
        free(handle->data);
    }
    fprintf(stderr, "Freeing handle: %p ...\n", handle);
    free(handle);

    if (loop.active_handles == 0)
    {
        // If there are no more active handles after this, stop the loop
        uv_stop(&loop);
    }
    
    printf("A handle was closed: %p (type=%d fd=%d).\n", (void*)handle, handle->type, handle->u.fd);
}


void on_walk_close_handle (uv_handle_t* handle, void* arg)
{
    fprintf(stderr, "Inside on_walk_close_handle(): %p ...\n", handle);
//    printf("Inside on_walk: NOP for now. arg=%s\n", (const char*)arg);
    uv_close(handle, on_close);
    printf("A handle was walked: %p (type=%d)\n", handle, handle->type);
}


void printrc (int rc, const char* funcName)
{
	char buf[1024];
	sprintf(buf, "%s()", funcName);
	printf("%-32s rc=%d\n", buf, rc);
	if (rc < 0)
	{
		printf("%d %s: %s\n", rc, uv_err_name(rc), uv_strerror(rc));
	}
}