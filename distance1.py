#!/usr/bin/python
import Adafruit_BBIO.ADC as ADC
import time
import math

sensor = "P9_37" #IR sensor pin
ADC.setup()

while True:
	reading = ADC.read(sensor) # values from 0 to 1
	voltage = reading * 1.65 #values from 0 to 1.65V
	distance = 13.93 * pow(voltage, -1.15)
	if distance > 80:
		print("Can't measure more than 80cm!")
	else:
		print("The reading, voltage and distance (in cm) are " + str(reading), str(voltage), str(distance))
	time.sleep(0.5) #loop every 500 milliseconds
