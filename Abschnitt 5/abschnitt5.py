#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author: Matt Hawkins
# Author's Git: https://bitbucket.org/MattHawkinsUK/
# Author's website: https://www.raspberrypi-spy.co.uk
import RPi.GPIO as GPIO
import smbus
import time
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
def main():
    sensor = LightSensor()
    try:
        while True:
            print("Lichtstärke : " + str(sensor.readLight()) + " lx")
            time.sleep(1)
    except KeyboardInterrupt:
        pass
if __name__ == "__main__":
    main()

#Wenn die Lux Anzahl im guten Bereich ist, soll auf der Matrixanzeige ein Symbol erscheinen.
#Andernfalls ein negatives Symbol