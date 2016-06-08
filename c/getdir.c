#include <errno.h>
#include <libgen.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int main (int argc, char* argv[])
{
	int rc;
	char* appname = argv[0];

	if (argc < 2)
	{
		fprintf(stderr, "Error: %s requires one argument\n", appname);
		exit(1);
	}

	char* path = argv[1];
/*
	printf("path=%s\n", path);
	char* realPath = realpath(path, NULL);
	if (realPath == NULL)
	{
		perror("Error (realpath):");
		exit(errno);
	}
	printf("realPath=%s\n", realPath);
	char* dir1 = dirname(realPath);
*/
	char* dir1 = dirname(path);
	if (chdir(dir1))
	{
		perror("Error");
		exit(errno);
	}

	char* cwd = getcwd(NULL, 0);
	printf("%s\n", cwd);	
	free(cwd);
}
