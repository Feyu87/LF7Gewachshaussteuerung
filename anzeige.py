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
    # Temperatur in einzelne Werte zerteilen
    temp = [int(i) for i in str(Temperatur)]
    

