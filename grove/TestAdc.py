import time
from grove.adc import ADC

adc = ADC()

while True:
    print(adc.read_voltage(0))
    time.sleep(1)
