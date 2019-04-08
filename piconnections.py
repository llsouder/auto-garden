from threading import Thread, Event
import eventlet
import RPi.GPIO as GPIO
import dht11

# initialize GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()

eventlet.monkey_patch()

LED = 20
GPIO.setup(LED, GPIO.OUT, initial=0)

LIGHT_SENSOR=21
GPIO.setup(LIGHT_SENSOR, GPIO.IN)


def read_dht11():
    instance = dht11.DHT11(pin=6)
    result = instance.read()
    if result.is_valid():
        return result.temperature*1.8+32, result.humidity
    return None


def turn_on_led(on):
    GPIO.output(LED, on)


def get_light_status():
    return GPIO.input(LIGHT_SENSOR)


class RaspberryPi(Thread):

    event = Event()
    temp_f = -1
    humidity = -1
    lights_on = True

    def __init__(self, consumer):
        self.consumer = consumer
        super(RaspberryPi, self).__init__()
        dht11_result = read_dht11()
        self.read_dht11(dht11_result)

    def poll_gpio(self):
        print("Starting GPIO loop...")
        while not self.event.isSet():
            eventlet.sleep(5)
            dht11_result = read_dht11()
            self.read_dht11(dht11_result)
            self.consumer.update_light_sensor(self.lights_on)
            self.lights_on = not self.lights_on

    def read_dht11(self, result):
        if result is not None:
            temp, humidity = result
            self.update_temp(temp)
            self.update_humidity(humidity)

    def update_temp(self, temp):
        if self.temp_f != temp:
            self.temp_f = temp
            self.send_temp()

    def send_temp(self):
        self.consumer.update_temp(self.temp_f)

    def update_humidity(self, humidity):
        if self.humidity != humidity:
            self.humidity = humidity
            self.send_humidity()

    def send_humidity(self):
        self.consumer.update_humidity(self.humidity)

    def run(self):
        self.poll_gpio()
