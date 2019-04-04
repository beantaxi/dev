// Thank you, https://luka.strizic.info/post/libuv-standard-input/output-and-TCP-input/output-example/
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <uv.h>
#include "common.h"
#include "console.h"
#include "hashtable.h"

// Global variables
char PATH[PATH_MAX];
int64_t counter = 0;
int rc;
uv_fs_t req_access;


int watchPath (uv_loop_t* loop, const char* path, uv_fs_event_cb cb)
{
	// Initialize an event and start a watch on it	
	uv_fs_event_t fsEvent;
	rc = uv_fs_event_init(loop, &fsEvent);
	printrc(rc, "uv_fs_event_init");
	if (rc < 0)
	{
		return rc;
	}

	// Start the watch. The event loop will not terminate as long as this watch is an active ref
	rc = uv_fs_event_start(&fsEvent, cb, path, UV_FS_EVENT_RECURSIVE);
	printrc(rc, "uv_fs_event_start");

	return rc;
}


void onAccess (uv_fs_t* req)
{
	printf("onAccess: result=%zd\n", req->result);
	printf("path=%s\n", req->path);
}


void onClose (uv_handle_t* handle)
{

}

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

		default:
		{
			fprintf(stderr, "Received unknown signal: %d\n", signum);
			break;
		}
	}
}

void checkForFile ()
{
	// Create loop
	uv_loop_t* loop = malloc(sizeof(uv_loop_t));
	rc = uv_loop_init(loop);
	printrc(rc, "uv_loop_init");
	
	// Make the access call
	rc = uv_fs_access(loop, &req_access, PATH, F_OK, onAccess);
	printrc(rc, "uv_fs_access");
	
	// Run the event loop
	rc = uv_run(loop, UV_RUN_DEFAULT);
	printrc(rc, "uv_run");
	
	// Close & shut down the event loop
	uv_stop(loop);

	rc = uv_loop_close(loop);
	printrc(rc, "uv_loop_close");
}


void wait_for_a_while (uv_idle_t* handle)
{
	counter++;
	printf("\r%lld", counter);
	if (counter >= 10e6)
	{
		int rc = uv_idle_stop(handle);
		printf("\n");
		printrc(rc, "uv_idle_start");
	}
}

void testIdleWatcher ()
{
	uv_idle_t idler;
	rc = uv_idle_init(uv_default_loop(), &idler);
	printrc(rc, "uv_idle_wait");
	
	rc = uv_idle_start(&idler, wait_for_a_while);
	printrc(rc, "uv_idle_start");
	
	printf("Idling ...\n");
	rc = uv_run(uv_default_loop(), UV_RUN_DEFAULT);
	printrc(rc, "uv_run");

	uv_loop_close(uv_default_loop());
}


void testHelloEventLoop ()
{
	const int LOOPCOUNT=1e6;

	for (int i=0; i<LOOPCOUNT; ++i)
	{
		// Create event loop
		uv_loop_t* loop = malloc(sizeof(uv_loop_t));
		rc = uv_loop_init(loop);
		printrc(rc, "uv_loop_init");
		
		rc = uv_run(loop, UV_RUN_DEFAULT);
		printrc(rc, "uv_run");

		uv_stop(loop);

		rc = uv_loop_close(loop);
		printrc(rc, "uv_loop_close");

		free(loop);
	}
}

void vanilla_access ()
{
	rc = access(PATH, F_OK);
	printrc(rc, "access");
}


void testHashtable ()
{
	GHashTable* hashTable = createHashtable();
	populateHashtable(hashTable);
	printHashTable(hashTable);
}

void onChange (uv_fs_event_t* fsEvent, const char* filename, int events, int status)
{
	printf("onChange(): filename=%s events=%d status=%d\n", filename, events, status);
	if (events & UV_RENAME)
	{
		printf("%s was renamed\n", filename);
	}
	if (events & UV_CHANGE)
	{
		printf("%s has changed\n", filename);
		rc = system("make build");
		printrc(rc, "system");
	}
}

void watchForChanges ()
{
	printf("Watching for changes to %s ...\n", PATH);

	// Create event loop
	uv_loop_t* loop = malloc(sizeof(uv_loop_t));
	rc = uv_loop_init(loop);
	printrc(rc, "uv_loop_init");
	
	// Initialize an event and start a watch on it	
	uv_fs_event_t fsEvent;
	fsEvent.cb = onChange;
	rc = uv_fs_event_init(loop, &fsEvent);
	printrc(rc, "uv_fs_event_init");
	rc = uv_fs_event_start(&fsEvent, fsEvent.cb, PATH, 0);
	printrc(rc, "uv_fs_event_start");
	
	// Run the event loop
	rc = uv_run(loop, UV_RUN_DEFAULT);
	printrc(rc, "uv_run");   
	
	// Stop & close the event loop
	uv_stop(loop);
	rc = uv_loop_close(loop);
	printrc(rc, "uv_loop_close");
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


void on_read_dummy (uv_stream_t* stream, ssize_t nread, const uv_buf_t* buf)
{

}

void on_read_echo (uv_stream_t* stream, ssize_t nread, const uv_buf_t* buf)
{
	fprintf(stderr, "In on_read_echo() ...\n");
	uv_write_t* reqWrite = initWriteRequest(onWrite);
	fprintf(stderr, "About to call uv_write() ...\n");
	// rc = uv_write(reqWrite, (uv_stream_t*)&pipe_stdout, buf, 1, reqWrite->cb);
	uv_buf_t bufToWrite = uv_buf_init(malloc(nread), nread);
	memcpy(bufToWrite.base, buf->base, nread);
	reqWrite->data = bufToWrite.base;
	rc = uv_write(reqWrite, (uv_stream_t*)&pipe_stdout, &bufToWrite, 1, reqWrite->cb);
	fprintf(stderr, "uv_write called. About to call printrc() ...\n");
	printrc(rc, "uv_write");
}

void simpleReadLoop ()
{
	// Initialize a pipe on stdin
	rc = uv_pipe_init(&loop, &pipe_stdin, 0);
	printrc(rc, "uv_pipe_init");
	rc = uv_pipe_open(&pipe_stdin, 0);
	printrc(rc, "uv_pipe_open");
	// Start a reader on the pipe
	rc = uv_read_start((uv_stream_t*)&pipe_stdin, on_alloc, on_read_dummy);
	printrc(rc, "uv_read_start");
	
	// Stop & close the event loop
	uv_walk(&loop, on_walk_close_handle, (void*)NULL);
	rc = uv_run(&loop, UV_RUN_DEFAULT);
	printrc(rc, "uv_run");
	rc = uv_loop_close(&loop);
	printrc(rc, "uv_loop_close");
}


void simpleEchoLoop ()
{
	// Create event loop
	rc = uv_loop_init(&loop);
	printrc(rc, "uv_loop_init");

	// Initialize stdout
	rc = uv_pipe_init(&loop, &pipe_stdout, 0);
	printrc(rc, "uv_pipe_init");
	rc = uv_pipe_open(&pipe_stdout, 1);
	printrc(rc, "uv_pipe_open");

	// Initialize stdin
	rc = uv_pipe_init(&loop, &pipe_stdin, 0);
	printrc(rc, "uv_pipe_init");
	rc = uv_pipe_open(&pipe_stdin, 0);
	printrc(rc, "uv_pipe_open");
	
	// Set up a reader on stdin
	rc = uv_read_start((uv_stream_t*)&pipe_stdin, on_alloc, on_read_echo);
	printrc(rc, "uv_read_start");

	// Set up a ctrl-c signal handler
	uv_signal_t sigint;
	rc = uv_signal_init(&loop, &sigint);
	printrc(rc, "uv_signal_init");
	rc = uv_signal_start_oneshot(&sigint, on_ctrl_c_kill_loop, SIGINT);
	printrc(rc, "uv_signal_start_oneshot");
	fprintf(stderr, "About to call uv_unref ...\n");
	uv_unref((uv_handle_t*)&sigint);
	
/*
	// Set up a ctrl-c signal handler
	uv_signal_t ctrl_c_handler;
	rc = uv_signal_init(&loop, &ctrl_c_handler);
	printrc(rc, "uv_signal_init");
	rc = uv_signal_start_oneshot(&ctrl_c_handler, on_ctrl_c_close_loop, SIGINT);
	uv_unref((uv_handle_t*)&ctrl_c_handler);
*/
	// Now that the reader is set up, run the loop
	fprintf(stderr, "About to run the loop ...\n");
	rc = uv_run(&loop, UV_RUN_DEFAULT);
	printrc(rc, "uv_run");

	fprintf(stderr, "\nThe run is done, baby! Time to shut down!\n\n");

	// Stop & close the event loop
	uv_walk(&loop, on_walk_close_handle, (void*)NULL);
	rc = uv_run(&loop, UV_RUN_DEFAULT);
	printrc(rc, "uv_run");
	rc = uv_loop_close(&loop);
	printrc(rc, "uv_loop_close");
}

void simpleConsoleWrite ()
{
	// Create event loop
	rc = uv_loop_init(&loop);
	printrc(rc, "uv_loop_init");

	// Initialize stdout
	rc = uv_pipe_init(&loop, &pipe_stdout, 0);
	printrc(rc, "uv_pipe_init");
	rc = uv_pipe_open(&pipe_stdout, 1);
	printrc(rc, "uv_pipe_open");
	
	 // Create a buffer
	const char* msg = "str!";
	uv_buf_t buf = uv_buf_init((char*)msg, strlen(msg));
	// Initialize a write request
	uv_write_t* reqWrite = initWriteRequest(onWrite);
	// Execute the write request with the buffer
	rc = uv_write(reqWrite, (uv_stream_t*)&pipe_stdout, &buf, 1, reqWrite->cb);
	printrc(rc, "uv_write");
		
/*
	// Create a buffer
	const char* msg = "Hello!\n";
	uv_buf_t buf = uv_buf_init((char*)msg, strlen(msg));
	// Initialize a write request
	uv_write_t* reqWrite = initWriteRequest(onWrite);
	// Execute the write request with the buffer
	rc = uv_write(reqWrite, (uv_stream_t*)&pipe_stdout, &buf, 1, reqWrite->cb);
	printrc(rc, "uv_write");
*/
	// Stop & close the event loop
	uv_walk(&loop, on_walk_close_handle, (void*)NULL);
	rc = uv_run(&loop, UV_RUN_DEFAULT);
	printrc(rc, "uv_run");
	rc = uv_loop_close(&loop);
	printrc(rc, "uv_loop_close");
}


int main (int argc, char* argv[])
{
/*
	if (argc < 2)
	{
		fprintf(stderr, "PATH expected as first argument\n");
		exit(1);
	}
*/
	// Treat the first argument as the path
	strncpy(PATH, argv[1], sizeof(PATH)/sizeof(char));
//	testIdleWatcher();
//	vanilla_access();
//	checkForFile();
//	testHelloEventLoop();
//	watchForChanges();   
//	testHashtable();

	simpleEchoLoop();
//	simpleConsoleWrite();
//	simpleConsole();
//	init_stdout();
//	simpleReadLoop();
//	signalTest();
}