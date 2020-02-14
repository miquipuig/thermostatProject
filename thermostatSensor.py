
import threading
import sys
if(len(sys.argv)>1 and sys.argv[1]=='test'):
    env='TST'
    from thermostatGPIO_test import tg
else:
    from thermostatGPIO import tg

class ThermostatSensor(object):
    
    def __init__(self, interval=10):
        self.interval=interval

        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True
        thread.start()

    def run(self):
        tg.callback_init()
        tg.readloop(self.interval)
        