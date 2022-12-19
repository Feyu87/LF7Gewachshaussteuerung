# Module importieren
import time
import datetime
import board
import adafruit_character_lcd.character_lcd_i2c as character_lcd
from Adafruit_LED_Backpack import SevenSegment

# segment der I2C Adresse 0x70 und die Displaydefinition zuweisen
segment = SevenSegment.SevenSegment(address=0x70)
# initialisierung der 7-Segmentanzeige
segment.begin()
# Definiere LCD Zeilen und Spaltenanzahl.
lcd_columns = 16
lcd_rows = 2
# Initialisierung I2C Bus
i2c = busio.I2C(board.SCL, board.SDA)
# Festlegen des LCDs in die Variable LCD
lcd = character_lcd.Character_LCD_I2C(i2c, lcd_columns, lcd_rows)

# Methode mit den Eingabewerten Temperatur und Luftfeuchtigkeit deklarieren
def Anzeige(Temperatur, Luftfeuchtigkeit):
    # Werte einmal in der Komandozeile ausgeben
    print('Temperatur: %.1f °C' %Temperatur)
    print('Feuchtigkeit: %.0f %' %Luftfeuchtigkeit)
    # Segmentanzeige aufrufen
    Segment(Temperatur, Luftfeuchtigkeit)
    LCD(Temperatur, Luftfeuchtigkeit)
    
# Methode für die Segmentanzeige
def Segment(Temperatur, Luftfeuchtigkeit):
    # Temperatur auf Ganzzahlen runden
    # TemperaturR ist der gerundete Wert
    TemperaturR = round(Temperatur)
    # und in einzelne Werte zerteilen
    temp = [int(i) for i in str(TemperaturR)]
    # Luftfeuchtigkeit auf Ganzzahlen runden (LuftfeuchtigkeitR ist der gerundete Wert)
    LuftfeuchtigkeitR = round(Luftfeuchtigkeit)
    # Luftfeuchtigkeit in einzelne Werte zerteilen
    luft = [int(i) for i in str(LuftfeuchtigkeitR)]
    # Segmentanzeige leeren
    segment.clear()
    # Temperaturwerte eingeben
    segment.set_digit(0, int(temp[0]))
    segment.set_digit(1, int(temp[1]))
    #Luftfeuchtigkeitswerte eingeben
    segment.set_digit(2, int(luft[0]))
    segment.set_digit(3, int(luft[1]))
    # Display aktualisieren
    segment.write_display()
    print('7-Segmentanzeige: success')

def LCD(Temperatur, Luftfeuchtigkeit):
    # LCD Display leeren
    lcd.clear
    # Hintergrundbeleuchtung anschalten
    lcd.backlight = True
    # Nachricht festlegen
    msg = 'Temp: ' + str(round(Temperatur, 1)) + '°C\nFeucht: ' + str(round(Luftfeuchtigkeit)) + '%'
    # Nachricht anzeigen
    lcd.message = msg
    print('LCD succes')

if(__name__ == '__main__'):
    Anzeige(27.3, 50.0)
