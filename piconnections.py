from threading import Thread, Event

import RPi.GPIO as GPIO
import eventlet

import dht11

# initialize GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()

eventlet.monkey_patch()

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


class RaspberryPi(Thread):
    event = Event()
    temp_f = -1
    humidity = -1
    light_status = False
    moisture = -1

    def __init__(self, websocket_updates):
        self.websocket = websocket_updates  # methods that receive updates from the pi.
        super(RaspberryPi, self).__init__()
        dht11_result = read_dht11()
        self.update_dth11_data(dht11_result)
        self.update_light_status()

    def poll_gpio(self):
        print("Starting GPIO loop...")
        while not self.event.isSet():
            eventlet.sleep(10)
            dht11_result = read_dht11()
            self.update_dth11_data(dht11_result)
            self.update_light_status()

    def update_dth11_data(self, result):
        if result is not None:
            temp, humidity = result
            self.update_temp(temp)
            self.update_humidity(humidity)

    def update_temp(self, temp):
        if self.temp_f != temp:
            self.temp_f = temp
            self.websocket.update_temp(temp)

    def update_humidity(self, humidity):
        if self.humidity != humidity:
            self.humidity = humidity
            self.websocket.update_humidity(humidity)

    def update_light_status(self):
        status = get_light_status()
        if self.light_status != status:
            self.light_status = status
            self.websocket.update_light_sensor(status)

    def run(self):
        self.poll_gpio()
