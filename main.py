import RPi.GPIO as GPIO
import dht11
import datetime

from flask import Flask
app = Flask(__name__)

# initialize GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()


@app.route("/")
def hello():
    # read data using pin 6
    instance = dht11.DHT11(pin=6)

    result = instance.read()
    if result.is_valid():
        F = result.temperature*1.8+32
        return "Last valid input: " + str(datetime.datetime.now()) + "<br>" \
               + "Temperature: %d F" % F + "<br>" \
               + "Humidity: %d %%" % result.humidity


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
