#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author: Matt Hawkins
# Author's Git: https://bitbucket.org/MattHawkinsUK/
# Author's website: https://www.raspberrypi-spy.co.uk
import RPi.GPIO as GPIO
import smbus
import time
import re
from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.core.virtual import viewport
from luma.core.legacy import text, show_message
from luma.core.legacy.font import proportional, CP437_FONT, TINY_FONT, SINCLAIR_FONT, LCD_FONT

if(GPIO.RPI_REVISION == 1):
    bus = smbus.SMBus(0)
else:
    bus = smbus.SMBus(1)
class LightSensor():
    def __init__(self):
    # Definiere Konstante vom Datenblatt
        self.DEVICE = 0x5c # Standard I2C Geräteadresse
        self.POWER_DOWN = 0x00 # Kein aktiver zustand
        self.POWER_ON = 0x01 # Betriebsbereit
        self.RESET = 0x07 # Reset des Data registers
 # Starte Messungen ab 4 Lux.
        self.CONTINUOUS_LOW_RES_MODE = 0x13
 # Starte Messungen ab 1 Lux.
        self.CONTINUOUS_HIGH_RES_MODE_1 = 0x10
 # Starte Messungen ab 0.5 Lux.
        self.CONTINUOUS_HIGH_RES_MODE_2 = 0x11
 # Starte Messungen ab 1 Lux.
 # Nach Messung wird Gerät in einen inaktiven Zustand gesetzt.
        self.ONE_TIME_HIGH_RES_MODE_1 = 0x20
 # Starte Messungen ab 0.5 Lux.
 # Nach Messung wird Gerät in einen inaktiven Zustand gesetzt.
        self.ONE_TIME_HIGH_RES_MODE_2 = 0x21
 # Starte Messungen ab 4 Lux.
 # Nach Messung wird Gerät in einen inaktiven Zustand gesetzt.
        self.ONE_TIME_LOW_RES_MODE = 0x23

    def convertToNumber(self, data):
 # Einfache Funktion um 2 Bytes Daten
 # in eine Dezimalzahl umzuwandeln
        return ((data[1] + (256 * data[0])) / 1.2)
    def readLight(self):
        data = bus.read_i2c_block_data(self.DEVICE,self.ONE_TIME_HIGH_RES_MODE_1)
        return self.convertToNumber(data)
def main(cascaded, block_orientation, rotate):
    # Matrix Gerät festlegen und erstellen. 
    serial = spi(port=0, device=1, gpio=noop()) 
    device = max7219(serial, cascaded=cascaded or 1, block_orientation=block_orientation, 
    rotate=rotate or 0) 
    # Matrix Initialisierung in der Konsole anzeigen 
    print("[-]")
    
    # Hallo Welt in der Matrix anzeigen 
    msg = "+"
    # Ausgegebenen Text in der Konsole Anzeigen 
    print("[-] Printing: %s" % msg) 
    show_message(device, msg, fill="white", font=proportional(CP437_FONT), scroll_delay=0.1)
    
    sensor = LightSensor()
    
    try:
        while True:
                if str(sensor.readLight()):
                    print("Lichtstärke gut: " + str(sensor.readLight()) + " lx")
                else:
                   print("Lichtstärke schlecht: " + str(sensor.readLight()) + " lx")
            time.sleep(1)
    except KeyboardInterrupt:
        pass
if __name__ == "__main__":
    # cascaded = Anzahl von MAX7219 LED Matrixen, standard=1 
    # block_orientation = choices 0, 90, -90, standard=0 
    # rotate = choices 0, 1, 2, 3, Rotate display 0=0°, 1=90°, 2=180°, 3=270°, standard=0 
    
    try:
        main(cascaded=1, block_orientation=90, rotate=0)
    except KeyboardInterrupt:
        pass

#Wenn die Lux Anzahl im guten Bereich ist, soll auf der Matrixanzeige ein Symbol erscheinen.
#Andernfalls ein negatives Symbol

#CHATGPT ALTERNATIVE

import Adafruit_DHT
import time
import smbus
import math
from Adafruit_LED_Backpack import Matrix8x8

# Initialisierung der 8x8 LED-Matrix
display = Matrix8x8.Matrix8x8(address=0x70)

# Initialisierung des Lichtsensors
bus = smbus.SMBus(1)
addr = 0x39 # Adresse des TSL2561-Sensors
# Kontroll- und Timing-Registerbits
CONTROL = 0x00
TIMING = 0x01
# Kanal 0 und Kanal 1 Lesebefehle
CHAN0_LOW = 0x0C
CHAN0_HIGH = 0x0D
CHAN1_LOW = 0x0E
CHAN1_HIGH = 0x0F

# Sensor-Typ und Pin-Nummer für den DHT11-Sensor
sensor = Adafruit_DHT.DHT11
pin = 4

while True:
    # Versuche, die Temperatur und Luftfeuchtigkeit vom DHT11-Sensor abzurufen
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

    # Wenn ein gültiger Wert abgerufen wurde, gib ihn auf dem LCD aus
    if humidity is not None and temperature is not None:
        display.clear()
        display.print_float(temperature)
        display.write_display()
    else:
        display.clear()
        display.print('Error')
        display.write_display()

    # Lese den Lichtsensor
    data = bus.read_i2c_block_data(addr, CONTROL, 2)
    timing = bus.read_i2c_block_data(addr, TIMING, 2)
    ch0 = data[1] * 256 + data[0]
    ch1 = data[3] * 256 + data[2]

    # Berechne die Lichtintensität in Lux
    if timing[0] == 0:
        timing[0] = 1
    ratio = float(ch1) / float(ch0)
    if ratio > 1.5:
        lux = (0.0304 * ch0) - (0.062 * ch0 * ((ratio) ** 1.4))
    elif ratio > 0.5:
        lux = (0.0224 * ch0) - (0.031 * ch1)
    else:
        lux = (0.0128 * ch0) - (0.0153 * ch1)
    lux = lux / timing[0]

    # Zeige ein lachendes oder weinendes Smiley basierend auf der Lichtintensität an
    if lux > 800:
        display.clear()
        display.set_pixel(1, 2, 1)
        display.set_pixel(6, 2, 1)
        display.set_pixel(2, 3, 1)
        display.set_pixel(5, 3, 1)
        display.set_pixel(2, 4, 1)
        display.set_pixel(5, 4, 1)
        display.set_pixel(2, 5, 1)
        display.set_pixel(3, 5, 1)
        display.set_pixel(4, 5, 1)
        display.write_display()
    else:
        display.clear()
        display.set_pixel(2, 2, 1)

