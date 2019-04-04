#include <uv.h>

typedef struct my_loop_s
{
    int value;
} my_loop_t;

extern int rc;
extern uv_loop_t loop;
extern my_loop_t myloop;
extern uv_pipe_t pipe_stdin;
extern uv_pipe_t pipe_stdout;
extern uv_pipe_t pipe_stderr;

int init_stdout ();
uv_write_t* initWriteRequest (uv_write_cb cb);
void on_alloc (uv_handle_t* handle, size_t size, uv_buf_t* buf);
void on_close (uv_handle_t* handle);
void on_walk_close_handle (uv_handle_t* handle, void* ignoreMe);
void printrc (int rc, const char* funcName);
