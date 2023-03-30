import Adafruit_DHT
import time
import board
import busio
import adafruit_character_lcd.character_lcd_rgb_i2c as character_lcd
import RPi.GPIO as GPIO
import math
from adafruit_led_backpack.matrix import Matrix8x8
from adafruit_led_backpack import i2c_lib
import csv

# Initialize I2C bus and LCD display
i2c = busio.I2C(board.SCL, board.SDA)
lcd_columns = 16
lcd_rows = 2
lcd = character_lcd.Character_LCD_RGB_I2C(i2c, lcd_columns, lcd_rows)

# Initialize LED Matrix
i2c_address = 0x70
i2c = busio.I2C(board.SCL, board.SDA)
display = Matrix8x8(i2c, address=i2c_address)

# Connect DHT11 sensor to GPIO 4
dht_sensor_pin = 4
dht_sensor = Adafruit_DHT.DHT11

# Connect Light sensor to GPIO 18
light_sensor_pin = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(light_sensor_pin, GPIO.IN)

# Funktion zur Ausgabe des Smiley-Icons
def display_smiley(smiley):
    if smiley == 'happy':
        display_pixels = [
            0b00111100,
            0b01000010,
            0b10100101,
            0b10000001,
            0b10100101,
            0b10011001,
            0b01000010,
            0b00111100
        ]
    elif smiley == 'sad':
        display_pixels = [
            0b00111100,
            0b01000010,
            0b10100101,
            0b10000001,
            0b10011001,
            0b10100101,
            0b01000010,
            0b00111100
        ]
    display.pixel_shader = display.Grayscale(2)
    display.pixel_span = (0, 0, 8, 8)
    for i in range(8):
        for j in range(8):
            pixel = (display_pixels[i] >> (7 - j)) & 1
            display.pixel(j, i, pixel)
    display.show()

# CSV-Datei initialisieren
csv_file = open('sensor_data.csv', 'a')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['Time', 'Temperature (C)', 'Humidity (%)', 'Light (lux)'])

# Endlosschleife für Sensor-Abfrage
while True:
    # Lese Sensor-Daten vom DHT11-Sensor
    humidity, temperature = Adafruit_DHT.read_retry(dht_sensor, dht_sensor_pin)

    # Lese Sensor-Daten vom Lichtsensor
    light_value = GPIO.input(light_sensor_pin)

    # Berechne Lux-Wert aus dem gemessenen Licht-Wert
    resistance = (float)(1023 - light_value) * 10 / light_value
    lux = math.pow(resistance / 10, 4)

    # Falls Lesefehler auftritt, setze auf Default-Werte
    if humidity is None or temperature is None:
        humidity, temperature = 0, 0

    # Aktualisiere LCD-Display mit neuen Daten
    lcd.clear()
    lcd.message = "Temp: {:.1f} C\nHumidity: {:.1f}%\nLight: {:.2f} lux".format(temperature, humidity, lux)

    # Gebe die Lichtwerte im Konsolenlog aus
    print("Lichtwert: {}\t Lux: {:.2f}".format(light_value, lux))

    # Aktualisiere LED-Matrix mit den neuen Daten
    if lux > 800:
        display_smiley('happy')
    else:
        display_smiley('sad')

    # Schreibe alle Werte in CSV-Datei
    now = time.strftime('%Y-%m-%d %H:%M:%S')
    csv_writer.writerow([now, temperature, humidity, lux])
    csv_file.flush()

    # Warte 5 Sekunden für nächste Abfrage
    time.sleep(5)
