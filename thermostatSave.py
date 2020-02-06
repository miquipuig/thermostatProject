import threading
from thermostatGPIO import tg


class ThermostatSave(object):
    def __init__(self, interval=1):
        self.interval = interval          
        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True
        thread.start()


    def run(self, interval=1):
        tg.saveloop(interval)