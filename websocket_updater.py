from threading import Thread, Event

import eventlet

eventlet.monkey_patch()

class WebsocketUpdater(Thread):
    event = Event()
    

    def __init__(self, garden, websocket_updates):
        self.websocket = websocket_updates  # methods that receive updates from the pi.
        self.garden = garden
        super(WebsocketUpdater, self).__init__()

    def run(self):
        print("Starting websocket updater loop...")
        while not self.event.isSet():
            eventlet.sleep(10)
            temp, humidity, light, moisture = self.garden.read_sensors()
            self.websocket.update_temp(temp)
            self.websocket.update_humidity(humidity)
            self.websocket.update_light_sensor(light)
            #there is no moisture! How dry I am!