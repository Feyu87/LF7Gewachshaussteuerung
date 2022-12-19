#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
import datetime
import board

#from Adafruit_LED_Backpack import SevenSegment
from adafruit_ht16k33.segments import Seg7x4

i2c = board.I2C()
segment = Seg7x4(i2c, address=0x70) #segment der I2C Adresse 0x70 und die Displaydefinition zuweisen

segment.fill(0) # Initialisierung des Displays. Muss einmal ausgeführt werden bevor das Display benutzt wird.

print ("STRG+C Druecken zum beenden.") #print Befehl für Ausgabe zum beenden des Scriptes

#Schleife welche dauerhaft die Zeit updated und sie auf dem Display anzeigt.
try:
  while(True):
    now = datetime.datetime.now()
    hour = now.hour
    minute = now.minute
    second = now.second

    segment.fill(0)

    # Anzeige für die Stunden.
    segment[0] =  str(int(hour / 10))     # Zehnerzahlen
    segment[1] =   str(hour % 10)         # Einerzahlen
    # Anzeige für die Minuten.
    segment[2] =   str(int(minute / 10))   # Zehnerzahlen
    segment[3] =   str(minute % 10)        # Einerzahlen
    #segment.colon = False
    
    if second % 2  == 0:
        segment.colon = True
    else:
        segment.colon = False             

    segment.show() # Wird benötigt um die Display LEDs zu updaten.

    time.sleep(1) # Warte eine Sekunde
except KeyboardInterrupt:
    segment.fill(0)
