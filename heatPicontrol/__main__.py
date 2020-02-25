# thermostatProject
# Copyright (C) 2020  Miquel Puig Gibert @miquipuig
 
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
 
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
 
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.

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
    ts.addCallbackFunctions(tv)
    tsave=ThermostatSave()  
    tt=ThermostatSensor()
    tw=ThermostatServer()
    tv.mainloop()
