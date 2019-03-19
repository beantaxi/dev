#include <stdio.h>
#include <glib.h>
#include "hashtable.h"


GHashTable* createHashtable ()
{
    GHashFunc hashFunc = g_str_hash;
    GEqualFunc eqFunc = g_str_equal;
    GHashTable* hashTable = g_hash_table_new(hashFunc, eqFunc);

    return hashTable;
}


void populateHashtable (GHashTable* hashTable)
{
    g_hash_table_insert(hashTable, "Chris", "13");
    g_hash_table_insert(hashTable, "John", "22");
    g_hash_table_insert(hashTable, "Peter", "19");
}


void printEntry (gpointer key, gpointer value, gpointer user_data)
{
    printf("%s => %s\n", (const char*)key, (const char*)value);
}

void printHashTable (GHashTable* hashTable)
{
    g_hash_table_foreach(hashTable, printEntry, NULL);
}