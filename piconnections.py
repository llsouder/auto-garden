#import RPi.GPIO as GPIO
#import dht11
import datetime

# initialize GPIO
# GPIO.setwarnings(False)
# GPIO.setmode(GPIO.BCM)
# GPIO.cleanup()


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