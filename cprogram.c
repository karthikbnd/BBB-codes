#include <stdio.h>
#include <fcntl.h>

double CtoF(double c)
{
        return (c * 9.0 / 5.0) + 32.0;
}

double temperature(char *string)
{
        int value = atoi(string);
        double millivolts = (value / 4096.0) * 1800;
        double temperature = (millivolts - 500.0) / 10.0;
        return temperature;
}

void main()
{
        int fd = open("/sys/devices/ocp.3/helper.15/AIN4", O_RDONLY);
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
                        double celsius = temperature(buffer);
                        double fahrenheit = CtoF(celsius);
                        printf("digital value: %s  celsius: %f  fahrenheit: %f\n", buffer, celsius, fahrenheit);
                        fprintf(f, "TempC: %f \t TempF:%f \n",celsius, fahrenheit);
			lseek(fd, 0, 0);
                }
		sleep(1);
		//fprintf(f, "TempC: %f \t TempF:%f \n",celsius, fahrenheit);
		//fclose(f);
        }
	fclose(f);
        close(fd);
}
