
import threading
import sys
from . import *
if(env=='testing'):
    from .gpio_test import tg
else:
    from .gpio import tg

class ThermostatSensor(object):
    
    def __init__(self, interval=10):
        self.interval=interval

        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True
        thread.start()

    def run(self):
        tg.callback_init()
        tg.readloop(self.interval)
        