import threading
from time import sleep
from gpiozero import DigitalInputDevice
from w1thermsensor import W1ThermSensor
import math
rainfall = 0
wind_count = 0
bucket_count = 0
radius_cm = 9.0
interval = 5
ADJUSTMENT = 1.18
CM_IN_A_KM = 100000.0
SECS_IN_AN_HOUR = 3600
BUCKET_SIZE = 0.2794

sensor = W1ThermSensor()
wind_speed_sensor = DigitalInputDevice(17, pull_up=True)
rain_sensor = DigitalInputDevice(27, pull_up=True)


def wind(time_sec):
    global wind_count
    circumference_cm = (2 * math.pi) * radius_cm
    rotations = wind_count / 2.0
    wind_count = 0

    dist_km = (circumference_cm * rotations) / CM_IN_A_KM

    km_per_sec = dist_km / time_sec
    km_per_hour = km_per_sec * SECS_IN_AN_HOUR

    return km_per_hour * ADJUSTMENT
 

def spin():
    global wind_count
    wind_count = wind_count + 1
 
def rain():
    global rainfall 
    global bucket_count
    bucket_count = bucket_count + 1
    rainfall = (bucket_count * BUCKET_SIZE - BUCKET_SIZE)
    print("Rainfall is currently "+str(rainfall)+"mm \n")

def temperature():
    while True:
        temp = sensor.get_temperature()
        print("The temperature is %s celsius \n" % temp)
        sleep(5)


windspeed = threading.Thread(name='wind', target=wind(interval))
raindata = threading.Thread(name='rain', target=rain)
tempdata = threading.Thread(name='temperature', target=temperature)

windspeed.start()
raindata.start()
tempdata.start()

wind_speed_sensor.when_activated = spin
rain_sensor.when_activated = rain

while True:
    sleep(interval)
    print ("The wind speed is "+str(round(wind(interval),2))+" kph \n")
    print("The cumulative rainfall is currently "+str(rainfall)+ "mm \n")


