import piconnections
from flask_socketio import SocketIO

from flask import Flask
app = Flask(__name__)
socketio = SocketIO(app)


@app.route("/toggle_led", methods=['GET'])
def toggle_led():
    print("on/off blinky blink!")
    return 'success'\


@app.route("/get_status", methods=['GET'])
def get_status():
    print("on/off blinky blink!")
    return 'success'


@app.route("/get_temp_and_humidity", methods=['GET'])
def get_temp_and_humidity():
    return piconnections.read_dht11();


if __name__ == '__main__':

    app.run(host='0.0.0.0', port=8000)
