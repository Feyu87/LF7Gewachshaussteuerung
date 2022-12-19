import RPi.GPIO as GPIO
import dht11
import board
import time
import busio
import adafruit_character_lcd.character_lcd_i2c as character_lcd

# initialize GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()
#Deklaration der Rows und Cols des LCD Displays

#aufbau einer while schleife zum wiederholten Messdurchfuehrung
lcd_columns = 16
lcd_rows = 2
i2c = busio.I2C(board.SCL, board.SDA)
lcd = character_lcd.Character_LCD_I2C(i2c, lcd_columns, lcd_rows)

try:
    while True:

        lcd.backlight = True
        #auslesen des Senosors DHT11 des pins 4 mit der Methode dht11. Daten werden in der Variable
        #instance hinterlegt
        instance = dht11.DHT11(pin=4)
        #die Werte der Variablen instance werden mit der Methode read() ausgelesen und in der Variablen
        #result gespeichert
        result = instance.read()
        # Konsolenausgabe mit dem String Temperatur und des Platzhaltes mit der einstelligen Dezimalausgabe formatiert
        # angehängt die Variable result mit der Methode temperature
        lcd.clear()
        scroll_msg = 'Temperatur: %-3.1f C*' % result.temperature
        lcd.message = scroll_msg
        for i in range(len(scroll_msg)):
            time.sleep(0.5)
            lcd.move_right()
        scroll_msg = "Feuchtigkeit: %-3.1f %%" % result.humidity
        for i in range(len(scroll_msg)):
            time.sleep(0.5)
            lcd.move_left()
        lcd.clear()
        lcd.backlight = False
        # Konsolenausgabe mit dem String Feuchtigkeit und des Platzhaltes mit der einstelligen Dezimalausgabe formatiert
        # angehängt die Variable result mit der Methode humidity
        #setzen eines breaks für 15 Sekunden, indem die aktuelle Zeit mit der festgehaltenen Startzeit subtrahiert wird.
        # ist der Wert 15.0 erreicht, so wird wieder zum schleifenanfang gesprungen und der Durchlauf beginnt solange endlos, bis das Programm
        # abgebrochen wird
except KeyboardInterrupt:
    lcd.clear()
    lcd.backlight = False