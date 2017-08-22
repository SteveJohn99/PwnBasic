#include <stdio.h>
#include <strings.h>

int main()
{
	int fd;
	char buf[32];
	
	bzero(buf, 32);
	fd = open("flag", 0);
	read(fd,buf, 32) ;
	write(1, buf, 32);
	close(fd);
}
