#include <stdio.h>
#include <sys/types.h>
#include <unistd.h>

int
main(int argc,char *argv[],char *envp[])
{
	unsigned long	i, j = 1000;

	printf("%d\n", getpid());

	for (i = 1; i < 99999999999; i++) {
		j = j / 132;
		j = j - 166;
		j = j * 178;
		j = j + 300;
	}

	return j;
}
