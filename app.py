from flask import Flask
from flask_socketio import SocketIO

import piconnections
from piconnections import RaspberryPi


class GpioInterface:

    def __init__(self, socket_arg):
        self.socket_io = socket_arg

    def update_temp(self, temp_f):
        self.socket_io.emit('current temp', {'data': temp_f})

    def update_humidity(self, humidity):
        self.socket_io.emit('current humidity', {'data': humidity})

    def update_light_sensor(self, lights_on):
        self.socket_io.emit('light status',
                            {'data':
                                 ('Light detected On' if lights_on else 'Light not detected Off')})


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
gpio_interface = GpioInterface(socketio)
pi = RaspberryPi(gpio_interface)
led_on = True


@app.route("/toggle_led", methods=['GET'])
def toggle_led():
    global led_on
    piconnections.turn_on_led(led_on)
    led_on = not led_on
    return 'success'


@app.route("/get_status", methods=['GET'])
def get_status():
    return 'success'


@socketio.on('connect')
def handle_connect():
    socketio.emit('after connect', {'data': 'testing the dance'})
    pi.send_temp()
    pi.send_humidity()
    pi.send_light_status()


if __name__ == '__main__':
    pi.start()
    socketio.run(app, host='0.0.0.0', port=8000, debug=True, use_reloader=False)
