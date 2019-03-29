import piconnections
from flask_socketio import SocketIO
from time import sleep
from flask import Flask
from piconnections import RaspberryPi


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socket_io = SocketIO(app)


@app.route("/toggle_led", methods=['GET'])
def toggle_led():
    print("on/off blinky blink!")
    return 'success'


@app.route("/get_status", methods=['GET'])
def get_status():
    print("on/off blinky blink!")
    return 'success'


@app.route("/get_temp_and_humidity", methods=['GET'])
def get_temp_and_humidity():
    return piconnections.read_dht11();


@socket_io.on('connect')
def handle_connect():
    print('received connect: ')
    socket_io.emit('after connect', {'data': 'testing the dance'})


def my_loop():
    counter = 0
    lights_on = True
    while not event.isSet():
        sleep(1)
        socket_io.emit('light status', {'data': ('lights On' if lights_on else'lights Off')})
        lights_on = not lights_on
        socket_io.emit('current temperature', {'data': counter})
        counter += 1


if __name__ == '__main__':
    thread = RaspberryPi(socket_io)
    thread.start()
    socket_io.run(app, debug=True)
