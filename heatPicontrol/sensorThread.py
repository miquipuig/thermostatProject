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
        