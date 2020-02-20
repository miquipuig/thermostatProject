import signal
import multiprocessing
import time
import os

from .screen import ThermostatScreen
from .server import ThermostatServer
from .dataService import ts
from .sensorThread import ThermostatSensor
from .saveThread import ThermostatSave

if __name__ == "__main__":

    tv=ThermostatScreen()
    ts.addCallbackFunction(tv.refresh_tempLabel)
    tsave=ThermostatSave()  
    tt=ThermostatSensor()
    tw=ThermostatServer()
    tv.mainloop()
