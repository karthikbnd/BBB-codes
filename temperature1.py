#!/usr/bin/python
import Adafruit_BBIO.ADC as ADC
import time
 
sensor_pin = 'P9_33' #temperature pin
 
ADC.setup()
 
while True:
    reading = ADC.read(sensor_pin)
    millivolts = (reading / 4096) * 1800  # 1.8V reference = 1800 mV
    temp_c = (millivolts - 500) / 10
    temp_f = (temp_c * 9/5) + 32
    print('mv=%d C=%d F=%d' % (millivolts, temp_c, temp_f))
    time.sleep(1)
