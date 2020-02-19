from logging.handlers import TimedRotatingFileHandler

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
# create a file handler
logname='logs/thermostatss.log'
handler = TimedRotatingFileHandler(logname, when="midnight", interval=1)
handler.suffix = "%Y%m%d"
# handler = logging.FileHandler('logs/thermostat.log')
handler.setLevel(logging.INFO)
# create a logging format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
# add the file handler to the logger
logger.addHandler(handler)

IMG_PATH='/resources/img/'
IMG_WEATHER_PATH='/resources/img/weather/'