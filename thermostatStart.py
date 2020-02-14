import signal
import multiprocessing
import time
import sys
#Import Project libraries
env='PRO'
if(len(sys.argv)>1 and sys.argv[1]=='test'):
    env='TST'


from thermostatScreen import ThermostatScreen
from thermostatServer import ThermostatServer
from thermostatService import ts
from thermostatSensor import ThermostatSensor
from thermostatSave import ThermostatSave



if __name__ == "__main__":

    tv=ThermostatScreen(env)
    ts.addCallbackFunction(tv.refresh_tempLabel)
    tsave=ThermostatSave()  
    tt=ThermostatSensor()
    tw=ThermostatServer()
    tv.mainloop()
