#include <uv.h>
#include "common.h"

int rc;

int main ()
{
    // Create event loop
    rc = uv_loop_init(&loop);
    //printrc(rc, "uv_loop_init");
    
    // Stop & close the event loop
    uv_stop(&loop);
    rc = uv_loop_close(&loop);
    //printrc(rc, "uv_loop_close");

    my_loop_t* myloop_ptr = &myloop;    
}