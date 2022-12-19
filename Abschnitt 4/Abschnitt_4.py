

import time
import busio
import adafruit_character_lcd.character_lcd_i2c as character_lcd
import RPi.GPIO  as GPIO
import dht11
import board
from adafruit_ht16k33.segments import Seg7x4
i2c = board.I2C()
segment = Seg7x4(i2c, address=0x70) 

segment.fill(0)
instance = dht11.DHT11(pin = 4)
result = instance.read()
# Definiere LCD Zeilen und Spaltenanzahl.
lcd_columns = 16
lcd_rows    = 2

# Initialisierung I2C Bus
i2c = busio.I2C(board.SCL, board.SDA)

# Festlegen des LCDs in die Variable LCD
lcd = character_lcd.Character_LCD_I2C(i2c, lcd_columns, lcd_rows, 0x21)

#definition/ inizalisiertung
print("Siebensegmentanzeige\n-------------------------------------\nTemperaturanzeige: linkes Segment\nLuftfeuchtigkeit: rechtes Segment")
try:
    while True:
        result = instance.read()
        #abfrage der Werte von dem sensor
        if(result.is_valid()):
            temp = [int(x) for x in str(round(result.temperature))]
            humid = [int(x) for x in str(round(result.humidity))]
            #teilt die angegeben Zahlen in 2 einzelne chars
            segment[0]= str(temp[0])
            segment[1] = str(temp[1])
            #schreibt die Zahl auf den jeweiligen Slot
            segment[2] = str(humid[0])
            segment[3]= str(humid[1])
             # Hintergrundbeleuchtung einschalten
            lcd.backlight = True

            # Zwei Worte mit Zeilenumbruch werden ausgegeben
            temp = str(round(result.temperature))
            feuchte = str(round(result.humidity))
            lcd.message = "Temperatur: "+ temp + "C\n"+"Feuchte: "+feuchte+"%"

            # 5 Sekunden warten
            time.sleep(5.0)

            # Cursor anzeigen lassen.
            lcd.clear()
    
except KeyboardInterrupt:
    # LCD ausschalten.
    lcd.clear()
    lcd.backlight = False
    segment.fill(0)
       #damit bei beenden das Programm nicht weiter Ziffern anzeigt
