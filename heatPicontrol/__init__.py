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

from logging.handlers import TimedRotatingFileHandler
import logging
import sys
import os
try:
    import tkinter.font as tkFont

except ImportError:
    import tkFont
#Crete runtime Data directories
LOGS_PATH='logs'
HISTORIC_PATH='historicData'
try:
    os.mkdir(LOGS_PATH)
    print("Directory " , LOGS_PATH ,  " Created ")
except:
    print("Directory " , LOGS_PATH ,  " already exists")
    
try:
    os.mkdir(HISTORIC_PATH)
    print("Directory " , HISTORIC_PATH ,  " Created ")
except:
    print("Directory " , HISTORIC_PATH ,  " already exists")
    

env='production'
if(len(sys.argv)>1 and sys.argv[1]=='test'):
    env='testing'
elif(len(sys.argv)>1 and sys.argv[1]=='staging'):
    env='staging'
    
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
# create a file handler
logname=LOGS_PATH+'/thermostat.log'
handler = TimedRotatingFileHandler(logname, when="midnight", interval=1)
handler.prefix = "%Y%m%d"
# handler = logging.FileHandler('logs/thermostat.log')
if(env=='testing'):
    handler.setLevel(logging.INFO)
elif(env=='staging'):
    handler.setLevel(logging.WARNING)
elif(env=='production'):
    handler.setLevel(logging.WARNING)

# create a logging format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
# add the file handler to the logger
logger.addHandler(handler)



#GLOBAL VARIABLES

PATHNAME = os.path.dirname(sys.argv[0])
print(PATHNAME)
PATHNAME = os.path.abspath(PATHNAME)+'/heatPicontrol'

IMG_PATH='/resources/img/'
IMG_WEATHER_PATH='/resources/img/weather/'
DAY_BREAF_PATH=HISTORIC_PATH+'/dayBreaf-'
COMPRESS_COUNTER=1 #25

#Colors
bg='#1d1d1d'
bg='#32174d'
tred='#ffa9b7'
tgreen='#a9fff1'
tblue='#a9b7ff'
tyellow='#fff1a9'
twhite='#ffffff'

