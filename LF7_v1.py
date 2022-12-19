import RPi.GPIO as GPIO
import dht11
import board
import time
import busio
import os
import sys
import anzeige

from adafruit_ht16k33.segments import Seg7x4

# initialize GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()
instance = dht11.DHT11(pin = 4)
result = instance.read()

while not result.is_valid():
	if result.is_valid:
		result = instance.read()

#print("Temperature: %-3.1f C" % result.temperature)
#print("Humidity: %-3.1f %%" % result.humidity)
anzeige.Anzeige(result.temperature, result.humidity)
time.sleep(15)


