import RPi.GPIO as GPIO
import dht11
import time

# initialize GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()

# read data using pin 14
instance = dht11.DHT11(pin = 4)
for i in range(20):
    print("%d. Messung" % (i+1))
    result = instance.read()

    while not result.is_valid():  # read until valid values
        result = instance.read()
    
    print("Temperature: %-3.f°C" % result.temperature)
    #print("Humidity: %-3.1f %%" % result.humidity)
    time.sleep(15)
