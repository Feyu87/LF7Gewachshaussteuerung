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
while True:
	#auslesen des Senosors DHT11 des pins 4 mit der Methode dht11. Daten werden in der Variable
	#instance hinterlegt
	instance = dht11.DHT11(pin=4)
	#die Werte der Variablen instance werden mit der Methode read() ausgelesen und in der Variablen
	#result gespeichert
	result = instance.read()
	#Konsolenausgabe einer Leerzeile
	print('			')
	# Konsolenausgabe eines String Wertes 'Neue Messung'
	print('Neue Messung')
	# Konsolenausgabe einer Leerzeile
	print('			')
	# Konsolenausgabe mit dem String Temperatur und des Platzhaltes mit der einstelligen Dezimalausgabe formatiert
	# angehängt die Variable result mit der Methode temperature
	print('Temperature: %-3.1f C*' % result.temperature)
	# Konsolenausgabe mit dem String Feuchtigkeit und des Platzhaltes mit der einstelligen Dezimalausgabe formatiert
	# angehängt die Variable result mit der Methode humidity
	print("Feuchtigkeit: %-3.1f %%" % result.humidity)
	#setzen eines breaks für 15 Sekunden, indem die aktuelle Zeit mit der festgehaltenen Startzeit subtrahiert wird.
	# ist der Wert 15.0 erreicht, so wird wieder zum schleifenanfang gesprungen und der Durchlauf beginnt solange endlos, bis das Programm
	# abgebrochen wird
	time.sleep(15.0)