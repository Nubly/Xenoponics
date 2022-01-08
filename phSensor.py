import time
import statistics as stats
from grove.adc import  ADC

# Connect the Grove PH Sensor to analog port A2
# SIG,NC,VCC,GND
adc = ADC()

# Reference voltage of ADC is 3.3v
adc_ref = 3.3
voltage_values = []
ph_values = [] 
count = 0

while True:
    try:

        #Voltage values  (mV) tested on: 11/15/2021
        #air temp of 68F
        #voltage_ph10 = 1945
        voltage_ph7 = 2644
        voltage_ph4 = 3126
        
        # Read sensor value(mV), convert to V
        voltage_value = adc.read_voltage(0)
        
        #to calculate pH accuratley above and below the reference voltage for pH7
        #the phStep value is calulated piecewise. ph4 > ph7 > p10
        ph = 7 + ((voltage_value-voltage_ph7)*(4 -7))/(voltage_ph4-voltage_ph7)
    
        print(f"Voltage: {voltage_value} mV pH: {'{:.2f}'.format(ph)}")
        voltage_values.append(voltage_value)
        ph_values.append(ph)
        if count == 50:
            print(f"Average voltage: {stats.mean(voltage_values)} Average ph: {round(stats.mean(ph_values), 2)}")
            exit(0)
        count = count + 1 
        time.sleep(1)

    except IOError:
        print ("Error")
