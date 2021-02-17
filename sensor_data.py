from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from threading import Timer

db = SQLAlchemy()


class SensorData(db.Model):
    time = db.Column(db.DateTime, primary_key=True)
    light = db.Column(db.Boolean)
    humidity = db.Column(db.Float)
    moisture = db.Column(db.Float)
    temperature = db.Column(db.Float)

    def __init__(self, light, humidity, moisture, temperature):
        self.time = datetime.now()
        self.light = light
        self.humidity = humidity
        self.moisture = moisture
        self.temperature = temperature


class SensorDataLogger():

    @staticmethod
    def __new_timer(function):
        DELAY = 1.0
        return Timer(DELAY, function)

    def __reset_timer(self, function):
        self.__timer = SensorDataLogger.__new_timer(function)
        self.__timer.start()

    def __log_data(self):
        light = False
        humidity = 0.0
        moisture = 0.0
        temperature = 0.0
        with self.__app.app_context():
            db.session.add(SensorData(light, humidity, moisture, temperature))
            db.session.commit()
        self.__reset_timer(self.__log_data)

    def __init__(self, app):
        self.__app = app
        self.__timer = SensorDataLogger.__new_timer(self.__log_data)

    def start(self):
        self.__timer.start()
