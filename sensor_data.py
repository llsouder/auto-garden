from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

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