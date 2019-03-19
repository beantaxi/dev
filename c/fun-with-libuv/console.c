#include <stdio.h>
#include <string.h>
#include <uv.h>
#include "console.h"

uv_pipe_t pipe_stdout;

int rc;



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

   
void helloWorld (uv_loop_t* loop)
{
    // Initialize new pipe
    rc = uv_pipe_init(loop, &pipe_stdout, 0);
    printrc(rc, "uv_pipe_init");    

    // Open pipe with stdout
    rc = uv_pipe_open(&pipe_stdout, 1);
    printrc(rc, "uv_pipe_open");
    
    // Initialize write request
    uv_write_t* reqWrite = malloc(sizeof(uv_write_t));

    // Write to pipe
    uv_buf_t data[1];
    const char* msg = "Hello World!\n";
    data[0].len = strlen(msg);
    data[0].base = msg;
    rc = uv_write(reqWrite, &pipe_stdout, data, 1, NULL);
    printrc(rc, "uv_write");
    // Cleanup? Not sure any is necessary
}


void simpleConsole ()
{
    //Create event loop
    uv_loop_t* loop = malloc(sizeof(uv_loop_t));
    rc = uv_loop_init(loop);
    printrc(rc, "uv_loop_init");

    helloWorld(loop);
    
    // Shutdown event loop
    printf("Console!\n");
}