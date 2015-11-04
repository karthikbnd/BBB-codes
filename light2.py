#!/usr/bin/python
import Adafruit_BBIO.ADC as ADC
import time
my_file = open("hello.txt","w") 
sensor_pin = 'P9_40' #Light sensor pin
 
ADC.setup()
my_file.write("the light voltage is \n") 
print('Reading\t\tVolts')
 
while True:
    reading = ADC.read(sensor_pin)
    volts = reading * 1.800
    v=str(volts)
    print('%f\t%f' % (reading, volts))
    my_file.write(v + '\n')
    time.sleep(1)
