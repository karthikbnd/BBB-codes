#include <stdio.h>
#include <fcntl.h>
#include <math.h>

double rtod(char *string)
{
        int value = atoi(string);
	double volts = (value / 4096.0) * 1.65;
	double distance = 13.93 * pow(volts, -1.15);
        return distance;
}

void main()
{
        int fd = open("/sys/devices/ocp.3/helper.15/AIN2", O_RDONLY);
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
                        double distance = rtod(buffer);
                        printf("digital value: %s \t distance(cm): %f\n", buffer, distance);
                        fprintf(f, "Reading: %s \t millivolts:%f \n",buffer, distance);
			lseek(fd, 0, 0);
                }
		sleep(1);
		//fprintf(f, "TempC: %f \t TempF:%f \n",celsius, fahrenheit);
		//fclose(f);
        }
	fclose(f);
        close(fd);
}
