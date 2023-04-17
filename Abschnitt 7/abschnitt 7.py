import RPi.GPIO as GPIO
import adafruit_character_lcd.character_lcd_i2c as character_lcd
import board
import busio
import csv
import datetime
import dht11
import os
import smbus
import time
from adafruit_ht16k33.segments import Seg7x4
from luma.core.interface.serial import spi, noop
from luma.core.legacy import text, show_message
from luma.core.legacy.font import proportional, CP437_FONT
from luma.led_matrix.device import max7219 as led

bus = smbus.SMBus(1)
DEVICE = 0x5c
ONE_TIME_HIGH_RES_MODE_1 = 0x20


class LightSensor():
    def read_light_sensor(self):
        data = bus.read_i2c_block_data(DEVICE, ONE_TIME_HIGH_RES_MODE_1)
        light_level = ((data[1] + (256 * data[0])) / 1.2)
        return light_level

    def set_day_light_offset(self):
        dt = datetime.datetime.now()
        return dt.time() <= datetime.time(6) and dt.time() >= datetime.time(18)


i2c = board.I2C()
serial = spi(port=0, device=1, gpio=noop())
device = led(serial, cascaded=1, block_orientation=90, rotate=0)
segment = Seg7x4(board.I2C(), address=0x70)
segment.fill(0)
lcd = character_lcd.Character_LCD_I2C(i2c, 16, 2, 0x21)


def display_on_segment(temp, humid):
    segment[0] = str(temp[0])
    segment[1] = str(temp[1])
    segment[2] = str(humid[0])
    segment[3] = str(humid[1])


def display_on_lcd(temp, humid):
    lcd.message = f"Temp: {str(temp[0]) + str(temp[1])} C\nHumidity: {str(humid[0]) + str(humid[1])}%"


def write_to_csv(temp, humid, light_level):
    file_exists = os.path.isfile("sensor_data.csv")

    with open("sensor_data.csv", mode="a", newline='') as sensor_data_file:
        fieldnames = ["timestamp", "temperature", "humidity", "light_level"]
        writer = csv.DictWriter(sensor_data_file, fieldnames=fieldnames)

        if not file_exists:
            writer.writeheader()

        writer.writerow({"timestamp": datetime.datetime.now(), "temperature": str(temp[0]) + str(temp[1]),
                         "humidity": str(humid[0]) + str(humid[1]), "light_level": light_level})


def main():
    instance = dht11.DHT11(pin=4)
    sensor = LightSensor()

    while True:
        result = instance.read()

        if (result.is_valid()):
            temp = [int(x) for x in str(round(result.temperature))]
            humid = [int(x) for x in str(round(result.humidity))]
            display_on_segment(temp, humid)
            display_on_lcd(temp, humid)

        light_level = sensor.read_light_sensor()
        print("Licht ausgeschaltet" if sensor.set_day_light_offset() else "Licht eingeschaltet")

        write_to_csv(temp, humid, light_level)
        show_message(device, get_light_level_symbol(light_level), fill="white", font=proportional(CP437_FONT),
                     scroll_delay=0.1)
        time.sleep(1)


def get_light_level_symbol(light_level):
    if light_level < 15000:
        return "+"
    elif light_level > 25000:
        return "-"
    else:
        return "="


if __name__ == "__main__":
    main()
