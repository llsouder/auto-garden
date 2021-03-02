


class TestGarden():

    def __init__(self):
        self.temp = 100
        self.humidity = 110
        self.light = True
        self.moisture = 300

    def turn_on_led(self, on):
        pass

    def read_sensors(self):
        self.temp += 1
        self.humidity += 1
        self.light = not self.light
        self.moisture -= 1
        return (self.temp, self.humidity, self.light,  self.moisture)
