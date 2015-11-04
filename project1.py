#!/usr/bin/python
import Adafruit_BBIO.ADC as ADC
import Adafruit_BBIO.GPIO as GPIO
import time
import math


my_file = open("Result.txt","w") # Write the results to a txt file

sensor_pin  = 'P8_10' # LED pin
sensor_pin1 = 'P9_33' # Temperature sensor pin
sensor_pin2 = 'P9_37' # IR sensor pin
sensor_pin3 = 'P9_38' # Force resistive sensor pin 
sensor_pin4 = 'P9_40' # Light sensor pin
 
ADC.setup()
GPIO.setup("P8_10", GPIO.OUT) #led OUT

my_file.write("Temperature_C \t Temperature_F \t Distance(cm) \t Force(v) \t Light(v) \n") 
 
while True:
	GPIO.output("P8_10", GPIO.HIGH)
	# Reading sensor values
	reading1 = ADC.read(sensor_pin1)
	reading2 = ADC.read(sensor_pin2)
	reading3 = ADC.read(sensor_pin3)
	reading4 = ADC.read(sensor_pin4)
	# Calculation of temperature
	millivolts = reading1 * 1800  # 1.8V reference = 1800 mV
    	temp_c = (millivolts - 500) / 10
    	temp_f = (temp_c * 9/5) + 32
	c = str(temp_c)
	f = str(temp_f)
    	print('mv=%d C=%d F=%d' % (millivolts, temp_c, temp_f))
	# Calculations of IR sensor
	voltage = reading2 * 1.65 #values from 0 to 1.65V
	distance = 13.93 * pow(voltage, -1.15)
	d = str(distance)
	if distance > 80:
		print("Can't measure more than 80cm!")
	else:
		print("The reading, voltage and distance (in cm) are " + str(reading2), str(voltage), str(distance))
    	# Calculations of FSR sensor
	voltf = reading3 * 1.800
    	f=str(voltf)
    	print('reading_FSR=%f \t Volt=%f' % (reading3, voltf))
    	# Calculations of Light sensor
	voltl = reading4 * 1.800
	l=str(voltl)
   	print('reading_Light=%f \t Volt=%f' % (reading4, voltl))
	my_file.write(c + '\t' + f + '\t' + d + '\t' + f + '\t' + l + '\n')
    	time.sleep(0.5)
