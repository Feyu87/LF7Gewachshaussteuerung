import RPi.GPIO as GPIO
import adafruit_character_lcd.character_lcd_i2c as character_lcd
import board
import busio
import csv
import datetime
import dht11
import os
import smbus
import ntplib
import time
from adafruit_ht16k33.segments import Seg7x4
from luma.core.interface.serial import spi, noop
from luma.core.legacy import text, show_message
from luma.core.legacy.font import proportional, CP437_FONT
from luma.led_matrix.device import max7219 as led

# Initialisierung des BH1750FVI Sensors
bus = smbus.SMBus(1)  # Use SMBus 1 for all Raspberry Pi models
DEVICE = 0x5c  # Default device I2C address
ONE_TIME_HIGH_RES_MODE_1 = 0x20  # Start measurement at 1 Lux


# Festlegung der Klasse Lichtsensor
class LightSensor():
    # Funktion zum ansprechen des Lichtsensors
    @staticmethod
    def read_light_sensor():
        # auslesen der Daten und transferierung in data variable
        data = bus.read_i2c_block_data(DEVICE, ONE_TIME_HIGH_RES_MODE_1)
        # auslesen der Daten in ein Array um das Lichtlevel zu definieren
        light_level = ((data[1] + (256 * data[0])) / 1.2)
        # Rückgabe der Lichtleveldaten
        return light_level

    @staticmethod
    def setDayLightOffset():
        # setzen der offset Flag auf false
        offset = False
        # Setzen der Tageszeit und der aktuellen Tageszeit
        dt = datetime.datetime.now().time()

        # Abfragen, ob die aktuelle Tageszeit vor 6 Uhr morgens und 18 Uhr abends liegt
        if datetime.time(6) <= dt <= datetime.time(18):
            # setzen des offsets auf wahr
            offset = True
        # nach Dämmerung und abends Rückgabe des Offsets
        return offset

    @staticmethod
    def getTime():
        ntp_client = ntplib.NTPClient()
        response = ntp_client.request('pool.ntp.org')
        current_time = datetime.datetime.fromtimestamp(response.tx_time)
        return current_time


# Initialisierung des Moduls MAX7219CWG Matrix 8x8
i2c = board.I2C()
# portaufruf und schnittstellenverbindung
serial = spi(port=0, device=1, gpio=noop())
# Geräteinitialisierung
device = led(serial, cascaded=1, block_orientation=90, rotate=0)
# Segmentinitialisierungen
segment = Seg7x4(board.I2C(), address=0x70)
segment.fill(0)  # Clear 7-segment display
# LCD Display Festlegungen
lcd = character_lcd.Character_LCD_I2C(i2c, 16, 2, 0x21)


# Es wird eine Endlosschleife zum lesen und ausgeben der Sensoren ausgeführt
def main():
    # Sensor für Temperatur und Luftfeuchtigkeit
    instance = dht11.DHT11(pin=4)
    # Lichtsensor wird festgelegt
    sensor = LightSensor()
    # Überprüfen, ob die CSV-Datei bereits existiert
    file_exists = os.path.isfile("sensor_data.csv")
    fieldnames = ["timestamp", "temperature", "humidity", "light_level"]

    while True:
        # das resultat der Daten wird im resultat abgelegt
        result = instance.read()
        # es wird abgefragt ob die ausgelesenen Daten valide sind
        if result.is_valid():
            # schreiben der ausgelesenen Temperaturwerte in die temp variable
            temp = str(round(result.temperature))
            # schreiben der ausgelesenen Feuchtigkeitswerte in die humid variable
            humid = str(round(result.humidity))
            # livedatenanzeige im 7 segment display
            segment[0] = temp[0]
            segment[1] = temp[1]
            # schreibt die Zahl auf den jeweiligen Slot
            segment[2] = humid[0]
            segment[3] = humid[1]
            # aktualisiert die Daten auf dem led
            lcd.message = f"Temp: {temp} C\nHumidity: {humid}%"
        # der Sensor des Lichtlevels wird ausgelesen
        light_level = sensor.read_light_sensor()
        # ist es Tageszeit, so wird kein Licht zugeführt
        if sensor.setDayLightOffset():
            print("Licht ausgeschaltet")
        # ansonsten wird das Licht eingeschaltet
        else:
            print('Licht eingeschaltet')

        # Schreiben der Sensordaten in die CSV-Datei
        with open("sensor_data.csv", mode="a", newline='') as sensor_data_file:
            writer = csv.DictWriter(sensor_data_file, fieldnames=fieldnames)

            # Schreiben der Spaltenüberschriften, wenn die Datei neu erstellt wurde
            if not file_exists:
                writer.writeheader()

            # Schreiben der Sensordaten in die Datei
            current_time = sensor.getTime()
            writer.writerow({
                "timestamp": str(current_time),
                "temperature": temp,
                "humidity": humid,
                "light_level": light_level
            })

        # ist das Lichtlevel unter 15000 Lux, so soll die Lichtstärke mit dem Symbol '+' angehoben werden
        if light_level < 15000:
            symbol = "+"
            # wartet eine Sekunde zum Einlesen neuer Werte
            time.sleep(1)
        # ist das Lichtlevel über 25000 Lux, so soll die Lichtstärke mit dem Symbol '-' gesenkt werden
        elif light_level > 25000:
            symbol = "-"
            # wartet eine Sekunde zum Einlesen neuer Werte
            time.sleep(1)
        else:
            # sollten beide Bedingungen nicht zutreffen, ist der optimale Lichtwert zwischen 15000 und 25000 Lux
            symbol = "="
            # wartet eine Sekunde zum Einlesen neuer Werte
            time.sleep(1)
        # aktualisieren der Matrix mit dem jeweiligen Symbol
        show_message(device, symbol, fill="white", font=proportional(CP437_FONT), scroll_delay=0.1)


# starten des Programms
if __name__ == "__main__":
    main()
