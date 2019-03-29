#import RPi.GPIO as GPIO
#import dht11
import datetime

# initialize GPIO
# GPIO.setwarnings(False)
# GPIO.setmode(GPIO.BCM)
# GPIO.cleanup()
from threading import Thread, Event
from time import sleep

def read_dht11():
    return "the temperature is too cold!"

# def read_dht11():
#     # read data using pin 6
#     instance = dht11.DHT11(pin=6)
#
#     result = instance.read()
#     if result.is_valid():
#         F = result.temperature*1.8+32
#         return "Last valid input: " + str(datetime.datetime.now()) + "<br>" \
#                + "Temperature: %d F" % F + "<br>" \
#                + "Humidity: %d %%" % result.humidity

class RaspberryPi(Thread):

    event = Event()

    def __init__(self, web_socket):
        self.socket_io = web_socket
        super(RaspberryPi, self).__init__()

    def poll_gpio(self):
        counter = 0
        lights_on = True
        while not self.event.isSet():
            sleep(1)
            self.socket_io.emit('light status', {'data': ('lights On' if lights_on else 'lights Off')})
            lights_on = not lights_on
            self.socket_io.emit('current temperature', {'data': counter})
            counter += 1

    def run(self):
        self.poll_gpio()
