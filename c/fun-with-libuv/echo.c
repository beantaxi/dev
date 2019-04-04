#include <stdlib.h>
#include <uv.h>
#include "common.h"

void on_ctrl_c_kill_loop (uv_signal_t* handle, int signum);
void on_read_echo (uv_stream_t* stream, ssize_t nread, const uv_buf_t* buf);
void onWrite (uv_write_t* handle, int status);

void on_ctrl_c_kill_loop (uv_signal_t* handle, int signum)
{
	switch (signum)
	{
		case SIGINT:
		{
			fprintf(stderr, "Received SIGINT\n");
			uv_stop(&loop);
			break;
		}
		
		case SIGTERM:
		{
			fprintf(stderr, "Received SIGTERM\n");
			uv_stop(&loop);
			break;
		}

		default:
		{
			fprintf(stderr, "Received unknown signal: %d\n", signum);
			break;
		}
	}
}


void on_read_echo (uv_stream_t* stream, ssize_t nread, const uv_buf_t* buf)
{
	fprintf(stderr, "In on_read_echo() ...\n");
	uv_write_t* reqWrite = initWriteRequest(onWrite);
	fprintf(stderr, "About to call uv_write() ...\n");
	// uv_write(reqWrite, (uv_stream_t*)&pipe_stdout, buf, 1, reqWrite->cb);
	uv_buf_t bufToWrite = uv_buf_init(malloc(nread), nread);
	memcpy(bufToWrite.base, buf->base, nread);
	reqWrite->data = bufToWrite.base;
	uv_write(reqWrite, (uv_stream_t*)&pipe_stdout, &bufToWrite, 1, reqWrite->cb);
}


void onWrite (uv_write_t* handle, int status)
{
	if (handle->data)
	{
		fprintf(stderr, "Freeing handle->data ...\n");
		free(handle->data);
	}
	if (handle)
	{
		fprintf(stderr, "Freeing handle ...\n");
		free(handle);
	}
}


int main ()
{
	// Create event loop0
	uv_loop_init(&loop);

	// Initialize stdout
	uv_pipe_init(&loop, &pipe_stdout, 0);
	uv_pipe_open(&pipe_stdout, 1);

	// Initialize stdin
	uv_pipe_init(&loop, &pipe_stdin, 0);
	uv_pipe_open(&pipe_stdin, 0);
	
	// Set up a reader on stdin
	uv_read_start((uv_stream_t*)&pipe_stdin, on_alloc, on_read_echo);

	// Set up a ctrl-c signal handler
	uv_signal_t sigint;
	uv_signal_init(&loop, &sigint);
	uv_signal_start_oneshot(&sigint, on_ctrl_c_kill_loop, SIGINT);
	uv_unref((uv_handle_t*)&sigint);

	// Now that everything is set up, run the loop
	fprintf(stderr, "About to run the loop ...\n");
	uv_run(&loop, UV_RUN_DEFAULT);

	fprintf(stderr, "\nThe run is done, baby! Time to shut down!\n\n");

	// Stop & close the event loop
	uv_walk(&loop, on_walk_close_handle, (void*)NULL);
	uv_run(&loop, UV_RUN_DEFAULT);
	uv_loop_close(&loop);
}