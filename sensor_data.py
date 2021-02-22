from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from threading import Timer
from json import JSONEncoder

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


class SensorDataEncoder(JSONEncoder):

    def default(self, obj):
        if isinstance(obj, SensorData):
            return {
                'time': obj.time.strftime('%H:%M:%S %m/%d/%Y'),
                'light': obj.light,
                'humidity': obj.humidity,
                'moisture': obj.moisture,
                'temperature': obj.temperature,
            }
        else:
            return super().default(obj)


class SensorDataLogger():

    @staticmethod
    def __new_timer(function):
        DELAY = 60.0
        return Timer(DELAY, function)

    def __reset_timer(self, function):
        self.__timer = SensorDataLogger.__new_timer(function)
        self.__timer.start()

    def __log_data(self):
        temperature, humidity, light, moisture = self.__read_sensors()
        with self.__app.app_context():
            db.session.add(SensorData(light, humidity, moisture, temperature))
            db.session.commit()
            for datum in SensorData.query.all():
                print(vars(datum))
        self.__reset_timer(self.__log_data)

    def __init__(self, app, read_sensors):
        '''
        Parameters:
            app: Flask app with a database connection
            read_sensors: a function that returns a tuple of sensor readings
        '''
        self.__app = app
        self.__read_sensors = read_sensors
        self.__timer = SensorDataLogger.__new_timer(self.__log_data)

    def start(self):
        '''Starts periodic logging'''
        self.__timer.start()
