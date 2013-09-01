#include <sys/types.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <errno.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <stdint.h>

int
main(int argc,char *argv[],char *envp[])
{
	unsigned char	csum = 0;
	int		i;

	if (argc != 2)
		return -1;

	for (i = 0; argv[1][i]; i++)
		csum += argv[1][i];

	printf("%x\n", csum);

	return 0;
}
