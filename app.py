from flask import Flask, request
from flask_socketio import SocketIO

import piconnections
from piconnections import RaspberryPi
from sensor_data import SensorData, SensorDataEncoder, db, SensorDataLogger

from functools import partial
import json


class WebSocketUpdates:

    def __init__(self, socket_arg):
        self.socket_io = socket_arg

    def update_temp(self, temp_f):
        self.socket_io.emit('current temp', {'data': temp_f})

    def update_humidity(self, humidity):
        self.socket_io.emit('current humidity', {'data': humidity})

    def update_light_sensor(self, lights_on):
        self.socket_io.emit('light status',
                            {'data': lights_on})


def read_sensors(pi):
    return (pi.temp_f, pi.humidity, pi.light_status, pi.moisture)


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
ws_updates = WebSocketUpdates(socketio)
pi = RaspberryPi(ws_updates)
led_on = True

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sensor_data.db'
db.init_app(app)
with app.app_context():
    db.create_all()
logger = SensorDataLogger(app, partial(read_sensors, pi))


@app.route("/toggle_led", methods=['GET'])
def toggle_led():
    global led_on
    piconnections.turn_on_led(led_on)
    led_on = not led_on
    return 'success'


@app.route("/get_status", methods=['GET'])
def get_status():
    return 'success'


@app.route("/sensor_log", methods=['GET'])
def sensor_log():
    ''' Returns sensor data history as list in JSON format'''
    return json.dumps(SensorData.query.all(), cls=SensorDataEncoder)


@socketio.on('connect')
def handle_connect():
    socketio.emit('after connect', {'data': 'testing the dance'})
    pi.send_temp()
    pi.send_humidity()
    pi.send_light_status()


if __name__ == '__main__':
    pi.start()
    logger.start()
    socketio.run(app, host='0.0.0.0', port=8000,
                 debug=True, use_reloader=False)
