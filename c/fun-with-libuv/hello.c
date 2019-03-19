#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <uv.h>
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


int main (int argc, char* argv[])
{
	if (argc < 2)
	{
		fprintf(stderr, "PATH expected as first argument\n");
		exit(1);
	}
	// Treat the first argument as the path
	strncpy(PATH, argv[1], sizeof(PATH)/sizeof(char));
//	testIdleWatcher();
//	vanilla_access();
//	checkForFile();
//	testHelloEventLoop();
//	watchForChanges();   
//	testHashtable();

	simpleConsole();
}