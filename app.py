from flask import Flask, request
from flask_socketio import SocketIO

from testgarden import TestGarden
#from piconnections import PiGarden
from websocket_updater import WebsocketUpdater
from sensor_data import SensorData, SensorDataEncoder, db, SensorDataLogger

from functools import partial
import json
from datetime import datetime

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


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
garden = TestGarden()
ws_updates = WebsocketUpdater(garden, WebSocketUpdates(socketio))
led_on = True

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sensor_data.db'
db.init_app(app)
with app.app_context():
    db.create_all()
logger = SensorDataLogger(app, garden.read_sensors)


@app.route("/toggle_led", methods=['GET'])
def toggle_led():
    global led_on
    garden.turn_on_led(led_on)
    led_on = not led_on
    return 'success'


@app.route("/get_status", methods=['GET'])
def get_status():
    return 'success'

# example of how to handle websocket events
# @socketio.on('connect')
# def handle_connect():
#     socketio.emit('connect msg', {'data': 'websocket connected'})

@app.route("/sensor_log", methods=['GET'])
def sensor_log():
    ''' 
    Parameters:
        start, end (str): Range of time to include in sensor log query
    Returns:
        sensor data history from <start> to <end> as list in JSON format
    '''
    def to_datetime(time: str) -> datetime:
        return datetime.strptime(time, SensorDataEncoder.time_format())

    res = SensorData.query
    start = request.args.get('start')
    if start:
        res = res.filter(SensorData.time >= to_datetime(start))
    end = request.args.get('end')
    if end:
        res = res.filter(SensorData.time <= to_datetime(end))
    return json.dumps(res.all(), cls=SensorDataEncoder)


if __name__ == '__main__':
    ws_updates.start()
    logger.start()
    socketio.run(app, host='0.0.0.0', port=8000,
                 debug=True, use_reloader=False)
