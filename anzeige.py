# Module importieren
import time
import datetime
from Adafruit_LED_Backpack import SevenSegment

# segment der I2C Adresse 0x70 und die Displaydefinition zuweisen
segment = SevenSegment.SevenSegment(address=0x70)
# initialisierung der 7-Segmentanzeige
segment.begin()

# Methode mit den Eingabewerten Temperatur und Luftfeuchtigkeit deklarieren
def Anzeige(Temperatur, Luftfeuchtigkeit):
    # Werte einmal in der Komandozeile ausgeben
    print('Temperatur: %.1f °C' %Temperatur)
    print('Feuchtigkeit: %.0f %' %Luftfeuchtigkeit)
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