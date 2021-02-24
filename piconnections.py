import RPi.GPIO as GPIO

import dht11

# initialize GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()

LED = 20
GPIO.setup(LED, GPIO.OUT, initial=0)

LIGHT_SENSOR = 21
GPIO.setup(LIGHT_SENSOR, GPIO.IN)


def read_dht11():
    instance = dht11.DHT11(pin=6)
    result = instance.read()
    if result.is_valid():
        return result.temperature * 1.8 + 32, result.humidity
    return None


def turn_on_led(on):
    GPIO.output(LED, on)


def get_light_status():
    return GPIO.input(LIGHT_SENSOR)


class PiGarden():
    def turn_on_led(self, on):
        turn_on_led(on)

    def read_sensors(self):
        result = read_dht11()
        if result is not None:
            temp, humidity = result
        else:
            temp=0
            humidity=0
        return temp, humidity, get_light_status(), 22
