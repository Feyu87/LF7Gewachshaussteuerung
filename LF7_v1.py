import RPi.GPIO as GPIO
import dht11
import board
import time
import os
import sys

from adafruit_ht16k33.segments import Seg7x4

# initialize GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()
#aufbau einer while schleife zum wiederholten Messdurchfuehrung
i=1
while True:
	#Sensor angeben und mittels der DHT11 Bibliothek auslesen
	instance = dht11.DHT11(pin=4)
	#instance auslesen
	Ergebnis = instance.read()
	# Variablen erstellen
	Temperatur = Ergebnis.termperature
	Luftfeuchtigkeit = Ergebnis.humidity
	# Temperatur Ausgeben auf eine Nachkommastelle genau
	print('Temp: %.1f °C' % Temperatur)
	# Luftfeuchtigkeit auf ganze Zahlen genau ausgeben
	print("Feuchtigkeit: %.0f %%" % Luftfeuchtigkeit)
	#15 sekunden abwarten
	time.sleep(15)
