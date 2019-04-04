#include <stdio.h>
#include <uv.h>
#include "common.h"

void onOpen (uv_fs_t* req);
void onWrite (uv_fs_t* req);


uv_fs_t req_open;
uv_fs_t req_write;
const char* PATH = "/tmp/test.txt";
const char* MSG = "MEAT";
void onOpen (uv_fs_t* req)
{
    fprintf(stderr, "onOpen\n");
    uv_file fd = (uv_file)req->result;
    fprintf(stderr, "fd=%d\n", fd);
    if (fd < 0)
    {
        printrc(fd, "onOpen");
    }

    uv_buf_t buf = uv_buf_init((char*)MSG, strlen(MSG));
    rc = uv_fs_write(&loop, &req_write, fd, &buf, 1, 0, onWrite);
    printrc(rc, "uv_fs_write");
}


void onWrite (uv_fs_t* req)
{
    fprintf(stderr, "onWrite() - result=%ld\n", req->result);
    if (req->result < 0)
    {
        printrc(req->result, "onWrite");
    }
}

int main ()
{
    printf("filewrite!\n");

    // Create event loop
    rc = uv_loop_init(&loop);
    printrc(rc, "uv_loop_init");

    // Try and open the file
//    int flags = UV_FS_O_CREAT | UV_FS_O_TRUNC | UV_FS_O_WRONLY;
//    int mode = UV_FS_SIR;
    int flags = O_WRONLY | O_CREAT | O_TRUNC;
    int mode = S_IWUSR;
    rc = uv_fs_open(&loop, &req_open, PATH, flags, mode, onOpen);
    printrc(rc, "uv_fs_open");
    

    // Run the event loop
    rc = uv_run(&loop, UV_RUN_DEFAULT);
    printrc(rc, "uv_run");

    // Stop & close the event loop
    uv_walk(&loop, on_walk_close_handle, (void*)NULL);
    rc = uv_run(&loop, UV_RUN_DEFAULT);
    printrc(rc, "uv_run");
    rc = uv_loop_close(&loop);
    printrc(rc, "uv_loop_close");
}