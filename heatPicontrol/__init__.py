from logging.handlers import TimedRotatingFileHandler
import logging
import sys

env='production'
if(len(sys.argv)>1 and sys.argv[1]=='test'):
    env='testing'
elif(len(sys.argv)>1 and sys.argv[1]=='staging'):
    env='staging'
    
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
# create a file handler
logname='logs/thermostatss.log'
handler = TimedRotatingFileHandler(logname, when="midnight", interval=1)
handler.suffix = "%Y%m%d"
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
IMG_PATH='/resources/img/'
IMG_WEATHER_PATH='/resources/img/weather/'

#Colors
bg='#1d1d1d'
bg='#32174d'
tred='#ffa9b7'
tgreen='#a9fff1'
tblue='#a9b7ff'
tyellow='#fff1a9'
twhite='#ffffff'