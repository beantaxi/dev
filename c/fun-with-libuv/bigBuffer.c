#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include "bigBuffer.h"

BigBuffer* bigBuffer_append (BigBuffer* bb, const char* buf, int n)
{
    bb = bigBuffer_resize(bb, bb->size + n);
    memcpy(bb->data + bb->iCur, buf, n);
    bb->iCur += n;

    return bb;
}


BigBuffer* bigBuffer_clear (BigBuffer* bb)
{
    fprintf(stderr, "Clearing big buffer: %p\n", bb);
    fprintf(stderr, "About to free bb->data: %p ...\n", bb->data);
    if (bb->data != NULL)
    {
        free(bb->data);
    }
    bb->iCur = 0;
    bb->size = 0;
    return bb;
}


BigBuffer* bigBuffer_create (long size)
{
    BigBuffer* bb = malloc(sizeof(BigBuffer));
    fprintf(stderr, "Created bb: %p\n", bb);
    bb->data = malloc(size);
    fprintf(stderr, "Created bb->data: %p\n", bb->data);
    memset(bb->data, 0, size);
    bb->iCur = 0;
    bb->size = size;

    return bb;
}


void bigBuffer_free (BigBuffer* bb)
{
    if (bb->data != NULL)
    {
        fprintf(stderr, "%p: freeing bb->data\n", bb->data);
        free(bb->data);
    }

    fprintf(stderr, "%p: freeing bb\n", bb);
    free(bb);
}




BigBuffer* bigBuffer_resize (BigBuffer* bb, long new_size)
{
    fprintf(stderr, "Resizing BigBuffer [%p] from %ld to %ld\n", bb, bb->size, new_size);
    fprintf(stderr, "Old bb->data: %p\n", bb->data);
    bb->data = realloc(bb->data, new_size);
    fprintf(stderr, "New bb->data: %p\n", bb->data);
    bb->size = new_size;

    return bb;
}

/*
int main ()
{
 Simple realloc(). Works.
    char* s = malloc(1);
    s = realloc(s, 6);
    memset(s, 0, 6);
    strncpy(s, "hello", strlen("hello"));
    fprintf(stderr, "%s", s);

    BigBuffer* bb = bigBuffer_create(0);
    const char* s = "Hello";
    int n = strlen(s);

//    bb->data = realloc(bb->data, n);
//    bb->size = strlen(s);

//    bb = bigBuffer_resize(bb, bb->size + n);
//    memcpy(bb->data + bb->iCur, s, strlen(s));
//    bb->iCur += strlen(s);
    bb = bigBuffer_append(bb, s, n);

    char* buf = malloc(n+1);
    memset(buf, 0, n+1);
    strncpy(buf, bb->data, bb->size);
    fprintf(stderr, "buf=%s\n", buf);

    fprintf(stderr, "Creating BigBuffer ...\n");
    BigBuffer* bb = bigBuffer_create(0);

    fprintf(stderr, "bb->size=%ld\n", bb->size);
    fprintf(stderr, "bb->iCur=%ld\n", bb->iCur);
    fprintf(stderr, "bb->data=%s\n", bb->data);

    bb = bigBuffer_append(bb, "Hello", strlen("Hello"));
    fprintf(stderr, "bb->size=%ld\n", bb->size);
    fprintf(stderr, "bb->iCur=%ld\n", bb->iCur);
    char* s = malloc(bb->size+1);
    memset(s, 0, bb->size+1);
    fprintf(stderr, "About to strncpy ...\n");
//    strncpy(s, bb->data,0 bb->size);
//    strncpy(s, bb->data, 1);
    strncpy(s, "H", 1);
    fprintf(stderr, "About to print bb->data ...\n");
    fprintf(stderr, "bb->data=%s\n", s);
    free(s);

    fprintf(stderr, "Clearing BigBuffer ...\n");
    bigBuffer_clear(bb);

}
*/