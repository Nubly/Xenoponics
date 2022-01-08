#!/usr/bin/env python3
import json
import sys
import time
import logging
import logging.handlers
import requests
import typer
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

# Logging
logger = logging.getLogger('xenologger')
logger.setLevel(logging.ERROR)

fileHandler = logging.handlers.RotatingFileHandler(
        'xenoponics.log',
        maxBytes=50000000,  # 50MB
        backupCount=20,     # Keep at most 1GB of logs
)

stdoutHandler = logging.StreamHandler(sys.stdout)

formatter = logging.Formatter(
        datefmt="%m-%d-%Y %H:%M:%S %Z",
        fmt='%(asctime)s %(levelname)s: %(message)s',
)

for handler in [stdoutHandler, fileHandler]:
    handler.setFormatter(formatter)
    logger.addHandler(handler)

# Requests TCP session and retries
sess = requests.Session()
retries = Retry(
        total=5,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
)

# HTTP headers/params constants
HEADERS = {
    "Accept-Encoding": "gzip, deflate, br",
    "Content-Type": "application/json",
    "Accept": "application/json",
}

# TODO: This type hinting is really fucking ugly lol, do something bout it
def get_post_data(data: dict[str, float, float, int, float]) -> dict[str, str]:
    """
    Helper function to return GraphQL friendly string for API call.
    """
    return { 
        'query': "mutation {\n"
        "    create_hydro(\n"
        f"        location: \"{data['location']}\"\n"
        f"        water_temp: {data['water_temp']}\n"
        f"        air_temp: {data['air_temp']}\n"
        f"        tds: {data['tds']}\n"
        f"        humidity: {data['humidity']}\n"
        "    ) {\n"
        "       location\n"
        "       water_temp\n"
        "       air_temp\n"
        "       tds\n"
        "       humidity\n"
        "   }\n"
        "}"
    }

def main(
    location: str = typer.Argument(
        default=None,
        help="A unique identifying string describing the location of the sensors.",
    ),
    # TODO: The below two don't work as arguments for some reason
    sensorPort: int = typer.Option(
        default=0,
        help="The I2C port that the TDS sensor is plugged into on the Pi.",
    ),
    sleepTime: int = typer.Option(
        default=300,
        help="The amount of time (in s) to wait before reporting to the database.",
    ),
    endpoint: str = typer.Option(
        "https://51aliens.space/api/v1/hydro",
        "--endpoint",
        "--api",
        "-e",
        help="The URL and endpoint which to POST data to.",
    ),
    debug: bool = typer.Option(
        False,
        help="Disable sensor reading for debugging purposes.",
    ),
):
    """
    Run the control script, taking a measurement and POSTing it to the GraphQL endpoint
    every SLEEPTIME seconds.
    """

    if not debug:

        # Sensor imports
        from lib import(
                grove_temperature_humidity_aht20 as gt,
                TDS as gtds,
        )
        from w1thermsensor import W1ThermSensor, Unit

        # Init sensors
        waterSensor = W1ThermSensor()
        airSensor = gt.GroveTemperatureHumidityAHT20()
        tdsSensor = gtds.GroveTDS(sensorPort)

        while True:

            # Read data
            tds = int(tdsSensor.TDS)
            airTemp, humidity = airSensor.read()
            water_temp = round(waterSensor.get_temperature(Unit.DEGREES_F), 2)
            air_temp = round((airTemp*1.8)+32, 2)
            humidity = round(humidity, 2)

            data = {
                "location": location,
                "water_temp": water_temp,
                "air_temp": air_temp,
                "tds": tds,
                "humidity": humidity
            }

            post_data = get_post_data(data)

            rsp = sess.post(endpoint, headers=HEADERS, data=json.dumps(post_data))

            if not rsp.ok:
                logger.error(
                    f'Something went wrong: {rsp.status_code}: {rsp.reason}\n'
                    f'Data: {json.dumps(data)}'
                )
            time.sleep(sleepTime)

    else:
        while True:
            print("Query: ",json.dumps(
                    get_post_data({
                    "location": "debug_location",
                    "water_temp": 50.0,
                    "air_temp": 75.0,
                    "tds": 1000,
                    "humidity": 25.0,
                })))

            time.sleep(sleepTime)

if __name__ == "__main__":
    typer.run(main)
