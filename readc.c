#include <sys/types.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <errno.h>
#include <fcntl.h>

#include <sys/time.h>
#include <signal.h>

static unsigned long	read_count;
static unsigned long	read_all_count = 0;
static unsigned long	read_times = 0;

static void
reset(void)
{
	struct itimerval	value;

	read_count = 0;

	value.it_value.tv_sec = 1; 
	value.it_value.tv_usec = 0;
	value.it_interval = value.it_value;
	if (setitimer(ITIMER_PROF, &value, NULL) == -1) {
		perror("setitimer");
		exit(-errno);
	}
}

static void
handler_sigprof(int signo)
{
	read_all_count += read_count;
	read_times++;
	printf("%d: %lu %lu\n", getpid(), read_count, read_all_count / read_times);
	reset();
}

static void
handler_sigint(int signo)
{
	printf("%lu\n", read_all_count / read_times);
	read_all_count = 0;
	read_times = 0;
}

int
main(int argc,char *argv[])
{
	struct sigaction	act;
	char	buf[1024];
	int	fd = open("/proc/version", O_RDONLY);
	if (fd < 0) {
		perror("open");
		exit(-errno);
	}

	act.sa_handler = handler_sigprof;
	if (sigfillset(&act.sa_mask) == -1) {
		perror("sigfillset");
		exit(-errno);
	}
	act.sa_flags = SA_RESTART;
	if (sigaction(SIGPROF, &act, NULL) == -1) {
		perror("sigaction");
		exit(-errno);
	}
	act.sa_handler = handler_sigint;
	if (sigaction(SIGINT, &act, NULL) == -1) {
		perror("sigaction");
		exit(-errno);
	}

	reset();

	while(1) {
		if (lseek(fd, 0, SEEK_SET) < 0) {
			perror("lseek");
			exit(-errno);
		}
		if (read(fd, buf, 1024) < 0) {
			perror("read");
			exit(-errno);
		}
		read_count ++;
	}

	return 0;
}
