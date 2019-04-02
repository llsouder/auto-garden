from threading import Thread, Event
import eventlet
import RPi.GPIO as GPIO
import dht11

# initialize GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()

eventlet.monkey_patch()


def read_dht11():
    instance = dht11.DHT11(pin=6)
    result = instance.read()
    if result.is_valid():
        return result.temperature*1.8+32, result.humidity
    return None


class RaspberryPi(Thread):

    event = Event()
    temp_f = -1
    humidity = -1
    lights_on = True

    def __init__(self, web_socket):
        self.socket_io = web_socket
        super(RaspberryPi, self).__init__()
        dht11_result = read_dht11()
        self.read_dht11(dht11_result)

    def poll_gpio(self):
        print("Starting GPIO loop...")
        while not self.event.isSet():
            eventlet.sleep(5)
            dht11_result = read_dht11()
            self.read_dht11(dht11_result)
            self.socket_io.emit('light status',
                                {'data':
                                     ('lights On' if self.lights_on else 'lights Off')})
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
        self.socket_io.emit('current temp', {'data': self.temp_f})

    def update_humidity(self, humidity):
        if self.humidity != humidity:
            self.humidity = humidity
            self.send_humidity()

    def send_humidity(self):
        self.socket_io.emit('current humidity', {'data': self.humidity})

    def run(self):
        self.poll_gpio()
