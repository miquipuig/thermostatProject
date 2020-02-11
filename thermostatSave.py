import threading
from thermostatGPIO import tg


class ThermostatSave(object):
    def __init__(self):        
        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True
        thread.start()


    def run(self):
        tg.saveloop(3)