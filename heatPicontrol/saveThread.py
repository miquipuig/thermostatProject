import threading
import sys
from . import *
if(env=='testing'):
    from .gpio_test import tg
else:
    from .gpio import tg

class ThermostatSave(object):
    def __init__(self):        
        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True
        thread.start()


    def run(self):
        tg.saveloop(3)