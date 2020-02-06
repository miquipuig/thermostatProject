
import threading
from thermostatGPIO import tg


class ThermostatSensor(object):
    
    def __init__(self, interval=10):
        self.interval=interval

        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True
        thread.start()

    def run(self):
        tg.callback_init()
        tg.readloop(self.interval(self.interval))
        