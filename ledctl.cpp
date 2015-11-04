#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <unistd.h>
 
int main(int argc, const char *argv[])
{
	if (argc != 3)
	{
	printf("Usage:\n");
	printf("\tledCtl <led> <on/off>\n");
	printf("\n");
	printf("<led>  : Number between 0-3\n");
	printf("<on/off>: 1 = on, 0 = off\n");

	return 1;
	}

	int ledNum = atoi(argv[1]);
	if (ledNum < 0 || ledNum > 3)
	{
		printf("<led>  : Number between 0-3\n");

		return 1;
	}

	char ledPath[1024];
	sprintf(ledPath, "/sys/class/leds/beaglebone\:green\:usr%d/brightness", ledNum);
	int fid = open(ledPath, O_WRONLY);

	int onOff = atoi(argv[2]);
	switch (onOff)
	{
		case 0:
			write(fid, "0", 1);
			break;
		case 1:
			write(fid, "1", 1);
			break;
		default:
			printf("<on/off>: 1 = on, 0 = off\n");
			return 1;
	}

	close(fid);

	return 0;
}
