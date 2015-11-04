#!/usr/bin/python
import Adafruit_BBIO.ADC as ADC
import time
 
sensor_pin = 'P9_38' #FSR sensor pin
 
ADC.setup()
 
print('Reading Voltage')
 
while True:
    reading = ADC.read(sensor_pin)
    volts = reading * 1.800
    print('%f' % (volts))
    time.sleep(0.5)
