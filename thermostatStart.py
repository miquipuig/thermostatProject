#Import Project libraries
from thermostatScreen import ThermostatScreen
from thermostatServer import ThermostatServer
from thermostatService import ts
from thermostatSensor import ThermostatSensor
from thermostatSave import ThermostatSave
# from thermostatSensorTuned import ThermostatSensor
import signal
import multiprocessing
import time
if __name__ == "__main__":
    tv=ThermostatScreen()
    ts.addCallbackFunction(tv.refresh_tempLabel)
    tsave=ThermostatSave()  
    tt=ThermostatSensor()
    tw=ThermostatServer()
    tv.mainloop()
