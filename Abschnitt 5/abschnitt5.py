import time
import datetime
import smbus, dht11, board, busio
import RPi.GPIO as GPIO
from adafruit_ht16k33.segments import Seg7x4
from luma.led_matrix.device import max7219 as led
from luma.core.interface.serial import spi, noop
from luma.core.legacy import text, show_message
from luma.core.legacy.font import proportional, CP437_FONT
import adafruit_character_lcd.character_lcd_i2c as character_lcd

# Initialize the BH1750FVI sensor
bus = smbus.SMBus(1)  # Use SMBus 1 for all Raspberry Pi models
DEVICE = 0x5c  # Default device I2C address
ONE_TIME_HIGH_RES_MODE_1 = 0x20  # Start measurement at 1 Lux


class LightSensor():
    def read_light_sensor(self):
        # Read data from the sensor and convert it to lux
        data = bus.read_i2c_block_data(DEVICE, ONE_TIME_HIGH_RES_MODE_1)
        light_level = ((data[1] + (256 * data[0])) / 1.2)
        return light_level

    def setDayLightOffset(self):
        offset = False
        dt = datetime.datetime.now()

        if (dt.time() <= datetime.time(6) and dt.time() >= datetime.time(18)):
            offset = True
            # nach sonnenaufgaban und bevor sonnen untergang
        return offset


# Initialize the MAX7219CWG matrix display
i2c = board.I2C()
serial = spi(port=0, device=1, gpio=noop())
device = led(serial, cascaded=1, block_orientation=90, rotate=0)
segment = Seg7x4(board.I2C(), address=0x70)
segment.fill(0)  # Clear 7-segment display
lcd = character_lcd.Character_LCD_I2C(i2c, 16, 2, 0x21)


# Loop to continuously read sensor data and update the matrix display
def main():
    instance = dht11.DHT11(pin=4)
    sensor = LightSensor()
    while True:
        result = instance.read()
        if (result.is_valid()):
            temp = [int(x) for x in str(round(result.temperature))]
            humid = [int(x) for x in str(round(result.humidity))]
            # Update 7-segment display
            segment[0] = str(temp[0])
            segment[1] = str(temp[1])
            # schreibt die Zahl auf den jeweiligen Slot
            segment[2] = str(humid[0])
            segment[3] = str(humid[1])
            # Update LCD display
            lcd.message = f"Temp: {str(temp[0]) + str(temp[1])} C\nHumidity: {str(humid[0]) + str(humid[1])}%"
        light_level = sensor.read_light_sensor()
        # print(sensor.setDayLightOffset)
        if (sensor.setDayLightOffset()):
            print("Licht ausgeschaltet")

        else:
            print('Licht eingeschaltet')
        # Evaluate the brightness level and assign a symbol
        if light_level < 15000:
            symbol = "+"
            time.sleep(1)
        elif light_level > 25000:
            symbol = "-"
            time.sleep(1)
        else:
            symbol = "="
            time.sleep(1)
        # Update the matrix display with the appropriate symbol
        show_message(device, symbol, fill="white", font=proportional(CP437_FONT), scroll_delay=0.1)


if __name__ == "__main__":
    main()


