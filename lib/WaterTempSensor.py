#!/usr/bin/python3
import time
from w1thermsensor import W1ThermSensor, Unit

sensor = W1ThermSensor()

while True:
    temperature = sensor.get_temperature(Unit.DEGREES_F)
    print("Temperature "+str(temperature)+"\n")
    time.sleep(1)







