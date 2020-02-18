import signal
import multiprocessing
import time
import sys
import os

env='PRO'
if(len(sys.argv)>1 and sys.argv[1]=='test'):
    env='TST'


from .screen import ThermostatScreen
from .server import ThermostatServer
from .dataService import ts
from .sensorThread import ThermostatSensor
from .saveThread import ThermostatSave



if __name__ == "__main__":

    tv=ThermostatScreen(env)
    ts.addCallbackFunction(tv.refresh_tempLabel)
    tsave=ThermostatSave()  
    tt=ThermostatSensor()
    tw=ThermostatServer()
    tv.mainloop()
