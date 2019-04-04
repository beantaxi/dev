#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <uv.h>
#include "common.h"
#include "console.h"

void helloWorld ();

const char* MEAT = "MEAT!";

uv_pipe_t pipe_stdout;
uv_pipe_t pipe_stdin;
uv_signal_t sig;

int rc;

void printf_uv_write_status (uv_write_t* cb, int status)
{
    printrc(status, "uv_write");
}


void on_control_c (uv_signal_t* handle, int signum)
{
    printf("Ctrl-C received! signum=%d\n", signum);
    uv_stop(&loop);
}


void signalTest ()
{
    // Create event loop
    rc = uv_loop_init(&loop);
    printrc(rc, "uv_loop_init");

    uv_signal_t sig;
    rc = uv_signal_init(&loop, &sig);
    printrc(rc, "uv_signal_init");
    rc = uv_signal_start(&sig, on_control_c, SIGTERM);
    printrc(rc, "uv_signal_start");
    rc = uv_signal_stop(&sig);
    printrc(rc, "uv_signal_stop");
    
    // Stop & close the event loop
    uv_walk(&loop, on_walk_close_handle, (void*)NULL);
    rc = uv_run(&loop, UV_RUN_DEFAULT);
    printrc(rc, "uv_run");
    rc = uv_loop_close(&loop);
    printrc(rc, "uv_loop_close");
}


void simpleConsole ()
{
    //Create event loop
    rc = uv_loop_init(&loop);
    printrc(rc, "uv_loop_init");

    helloWorld();
/*
    uv_signal_t sig;
    rc = uv_signal_init(&loop, &sig);
    printrc(rc, "uv_signal_init");
    rc = uv_signal_start(&sig, on_control_c, SIGTERM);
    printrc(rc, "uv_signal_start");
    uv_unref((uv_handle_t*)&sig);
    rc = uv_signal_stop(&sig);
    printrc(rc, "uv_signal_stop");
*/
    // Stop & close the event loop
    uv_walk(&loop, on_walk_close_handle, (void*)NULL);
    rc = uv_run(&loop, UV_RUN_DEFAULT);
    printrc(rc, "uv_run");
    rc = uv_loop_close(&loop);
    printrc(rc, "uv_loop_close");
}

/*
void on_alloc (uv_handle_t* handle, size_t size, uv_buf_t* buf)
{
    printf("In on_alloc(): size=%ld\n", size);
    buf->len = size;
    buf->base = malloc(buf->len);
}
*/

void on_read (uv_stream_t* stream, ssize_t nread, const uv_buf_t* buf)
{
    printf("In on_read(): nread=%ld buf->len=%ld\n", nread, buf->len);
    char* data = (char *)malloc(nread);
    strncpy(data, buf->base, nread);
    printf("%s\n", data);
    free(data);
}

void helloWorld ()
{
    // Initialize new pipe
//    rc = uv_pipe_init(loop, &pipe_stdout, 0);
//    printrc(rc, "uv_pipe_init");    

    // Initialize a signal handler & start it listening to Ctrl-C
    rc = uv_signal_init(&loop, &sig);
    printrc(rc, "uv_signal_init");
    rc = uv_signal_start(&sig, on_control_c, SIGINT);
    printrc(rc, "uv_signal_start");
    // uv_unref so to make the signal handler a 'weak reference' on the event loop
    uv_unref((uv_handle_t*)&sig);
    
    // Open pipe to stdout
    rc = uv_pipe_init(&loop, &pipe_stdout, 0);
    printf("About to open pipe ...\n");
    rc = uv_pipe_open(&pipe_stdout, 1);
    printrc(rc, "uv_pipe_open");
    
    // Initialize write request & set its callback
    uv_write_t* reqWrite = malloc(sizeof(uv_write_t));
    reqWrite->cb = printf_uv_write_status;

    // Write to pipe
    // Writing in libuv is not trivial. All data is binary, so for everything you want to write,
    // you need to provide the data and a length. That's literally all uv_buf_t is:
    // 
    //    typedef struct uv_buf_t {
    //       char* base;
    //       size_t len;
    //    } uv_buf_t
    // 
    // Also, uv_write takes an array of uv_buf_t. So just to write a single string, you need to create
    // an array of uv_buf_t[1] (length=1), assign .base to your string, and assign strlen of your string 
    // to .len
    //
    // That's a lot of work for hello world.
    const char* msg = "Hello World!\n";
    uv_buf_t data[1];
    data[0].base = (char*)msg;
    data[0].len = strlen(data[0].base);
    rc = uv_write(reqWrite, (uv_stream_t*)&pipe_stdout, data, 1, NULL);
    printrc(rc, "uv_write");
    
    // Read from stdin
    rc = uv_pipe_init(&loop, &pipe_stdin, 0);
    printrc(rc, "uv_pipe_init");
    rc = uv_pipe_open(&pipe_stdin, 0);
    printrc(rc, "uv_pipe_open");
    rc = uv_read_start((uv_stream_t*)&pipe_stdin, on_alloc, on_read);

    // Run the loop, so it can read from stdin
    rc = uv_run(&loop, UV_RUN_DEFAULT);
    printrc(rc, "uv_run");
}