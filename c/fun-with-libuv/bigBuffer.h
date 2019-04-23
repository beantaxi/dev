typedef struct BigBuffer_s
{
    char* data;
    long iCur;
    long size;
} BigBuffer;

BigBuffer* bigBuffer_append (BigBuffer* bb, const char* buf, int n);
BigBuffer* bigBuffer_clear (BigBuffer* bb);
BigBuffer* bigBuffer_create (long size);
BigBuffer* bigBuffer_resize (BigBuffer* bb, long new_size);
