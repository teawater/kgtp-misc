#include <stdio.h>
#include <sys/types.h>
#include <unistd.h>

int
main(int argc,char *argv[],char *envp[])
{
	unsigned long	i, j;

	printf("%d\n", getpid());

	for (i = 1; i < 99999999999; i++) {
		j = i / 13;
		j = j - 13;
		j = j * 13;
		j = j + 13;
	}

	return j;
}
