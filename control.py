#!/usr/bin/python3
from grove import grove_temperature_humidity_aht20 as gt
from grove import TDS as gtds
import time
from matplotlib import pyplot as plt
import numpy as np
from datetime import datetime
#water temp sensor
from w1thermsensor import W1ThermSensor


WaterSensor = W1ThermSensor()
AirSensor = gt.GroveTemperatureHumidityAHT20()
tdsSensor = gtds.GroveTDS(2)


fig, axis = plt.subplots(4)
axis[0].set_title('Air Temperature v. Time')
axis[0].set_xlabel('Time')
axis[0].set_ylabel('Temperature (F)')

axis[1].set_title('Humidity v. Time')
axis[1].set_xlabel('Time')
axis[1].set_ylabel('Humidity (%)')

axis[2].set_title('Water Temperature v. Time')
axis[2].set_xlabel('Time')
axis[2].set_ylabel('Temperature (F)')

axis[3].set_title('TDS v. Time')
axis[3].set_xlabel('Time')
axis[3].set_ylabel('TDS (ppm)') 

AirTemperatures = []
WaterTemperatures = []
times = []
humidities = []
tdsReadings = []

count = 0

with open("data.log", "w") as datafile:
    while True:
        time.sleep(300)
        AirTemperature, humidity = AirSensor.read()
        WaterTemperature = WaterSensor.get_temperature()
        tds = tdsSensor.TDS
        
        if count % 30 == 0:
            axis[0].plot(times, AirTemperatures)
            axis[1].plot(times, humidities)
            axis[2].plot(times, WaterTemperatures)
            axis[3].plot(times, tdsReadings)
            fig.savefig("TempGraph.png")
             
        AirTemperature = (AirTemperature*1.8)+32
        WaterTemperature = (WaterTemperature*1.8)+32

        AirTemperatures.append(AirTemperature)
        humidities.append(humidity)
        WaterTemperatures.append(WaterTemperature)
        tdsReadings.append(tds)
        times.append(datetime.now())
        
        count += 1

        plt.gcf().autofmt_xdate()
        plt.pause(0.01)

        formatted = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} AirTemp (F): {round(AirTemperature, 2)} Humidity: {round(humidity, 2)}% WaterTemp (F): {round(WaterTemperature, 2)} TDS: {round(tds, 2)}\n"
        print(formatted)
        datafile.write(formatted)
    
