#include <stdio.h>

int c = 0;

int 
main (int argc, char *argv[], char *envp[]) 
{
	if (argc > 1)
		c = atoi(argv[1]);

	printf("%d\n", getpid());

	while(1) {
		c += 1;
		printf("%d\n", c);
		sleep(1);
	}

	return 0;
}

