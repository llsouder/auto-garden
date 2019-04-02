from flask_socketio import SocketIO
from flask import Flask
from piconnections import RaspberryPi
import piconnections


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
pi = RaspberryPi(socketio)


@app.route("/toggle_led", methods=['GET'])
def toggle_led():
    return 'success'


@app.route("/get_status", methods=['GET'])
def get_status():
    return 'success'


@socketio.on('connect')
def handle_connect():
    print('received connect: ')
    socketio.emit('after connect', {'data': 'testing the dance'})
    pi.send_temp()
    pi.send_humidity()


if __name__ == '__main__':
    pi.start()
    socketio.run(app, host='0.0.0.0', port=8000)
