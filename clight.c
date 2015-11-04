#include <stdio.h>
#include <fcntl.h>

double rtov(char *string)
{
        int value = atoi(string);
	double millivolts = (value / 4096.0) * 1800;
        return millivolts;
}

void main()
{
        int fd = open("/sys/devices/ocp.3/helper.15/AIN1", O_RDONLY);
	FILE *f = fopen("result.txt", "w");

	if (f == NULL)
	{
        	printf("Error opening file!\n");
        	exit(1);
	}

        while (1)
	{
                char buffer[1024];
                int ret = read(fd, buffer, sizeof(buffer));
                if (ret != -1)
		{
                        buffer[ret] = NULL;
                        double millivolts = rtov(buffer);
                        printf("digital value: %s \t light(millivolts): %f\n", buffer, millivolts);
                        fprintf(f, "Reading: %s \t millivolts:%f \n",buffer, millivolts);
			lseek(fd, 0, 0);
                }
		sleep(1);
		//fprintf(f, "TempC: %f \t TempF:%f \n",celsius, fahrenheit);
		//fclose(f);
        }
	fclose(f);
        close(fd);
}
