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

from datetime import datetime,timedelta
import numpy as np
import random
import os
from .historicData import ThermostatHistory
from . import *
import requests
import json

class ThermostatService:   
    temp = 19
    humidity = 44
    
    #weather
    weatherTemp = 20
    weatherTemp_min=20
    weatherTemp_max=20
    weatherHumidity=50
    weatherIcon='01d'
    weatherDesciption=' '
    
    #Inital Temperatures
    desiredT = 21.5
    desiredMoonT=19.5
    desiredSunT=20
    #Day night Control
    moonSun='sun' #Day or night
    sunTime="08:00"
    moonTime="00:45"
    dayNightChange=True
    
    

    #States
    online=True
    ip=None
    ip_external=None
    errors=False
    power = None
    started = False #
    tAchieved= False # desired temperature = temperature
    refreshDesiredConf=False #Refresh visualization with a configuration change
    refreshDataListener=False #Refresh visualization with and environment change
    fakecounter=0
    weatherCounter=50
       
    onTimer= datetime.now()
    offTimer= datetime.now()
    
    #Configuration parameters
    onTime=1 #minutes Needed turned on time to turn on
    offTime=1 #minutes Needed turned off time to turn off
    precisionRange=0.1
    
    th=ThermostatHistory()
    
    tvCallbackFunction=None
    compressCounter=0
    def __init__(self, power=False):
        self.temp 
        self.desiredT 
        self.power = power
    
    def updateHomeClimate(self, temp, relativeHumidity):
        
        self.updateConnection()
        self.updateWheather()
        self.temp = np.around(temp, decimals=1)
        self.th.historicData.append([datetime.now(),temp,self.desiredT,relativeHumidity,self.weatherHumidity])
        self.humidity = relativeHumidity
        self.refreshDataListener=True
        
        if(self.compressCounter<COMPRESS_COUNTER):
            self.compressCounter+=1
        else:
            try:
                self.th.compress()
            except Exception as ex:
                logger.error('Compress Error')
                logger.error(ex)
            self.compressCounter=0
        # self.th.storeData() -> Now included inside compress function
        
    def addCallbackFunctions(self, functions):
        self.tv=functions
    
    def updateConnection(self):
        stream = os.popen("ip addr | grep 'state UP' -A2 | tail -n1 | awk '{print $2}' | cut -f1  -d'/'")
        self.ip = stream.read()
        stream2 = os.popen("curl ifconfig.co 2>nul")
        self.ip_external = stream2.read()
        # print(self.ip_external)
    def updateWheather(self):
        if(self.weatherCounter>10):
            self.weatherCounter=0
            url = 'https://api.openweathermap.org/data/2.5/weather?zip=08014,es&appid=35bef01f2be23b616aa0457916b79b5d&lang=ca'
            try:
                response = requests.get(url)
                resp_dict=json.loads(response.text)
                self.weatherTemp=np.around(resp_dict['main']['temp']-273.15,decimals=1)
                self.weatherTemp_min=np.around(resp_dict['main']['temp_min']-273.15,decimals=1)
                self.weatherTemp_max=np.around(resp_dict['main']['temp_max']-273.15,decimals=1)
                self.weatherHumidity=np.around(resp_dict['main']['humidity'],decimals=0)
                self.weatherIcon=json.loads(json.dumps(resp_dict['weather'][0]))['icon']
                self.weatherDesciption=json.loads(json.dumps(resp_dict['weather'][0]))['description']
                self.online=True
            except Exception as ex:
                self.online=False
                logger.error(ex)
        self.weatherCounter+=1
        
    def setTemperature(self, temp):
        if(temp<29|temp>9):
            self.desiredT = temp
            self.dayNightSaveTemperature()
            self.refreshDataListener=True
    
    def ecoState(self):
        if(self.moonSun=='sun'):
            if(self.desiredT<=21 and self.power):
                return True
        else:
            if(self.desiredT<20 and self.power):
                return True
        return False
                    
    def increaseTemperature(self):
        if(self.desiredT<28):
            self.desiredT =round(self.desiredT + 0.1,1)
            self.tv.refresh_tempLabel()
            self.refreshDesiredConf=True
            self.dayNightSaveTemperature()
        self.resetSaveHeater()
   
    def decreaseTemperature(self):
        if(self.desiredT>10):
            self.desiredT = round(self.desiredT - 0.1,1)
            self.tv.refresh_tempLabel()
            self.refreshDesiredConf=True
            self.dayNightSaveTemperature()
        self.resetSaveHeater()
        
    def increaseSunTime(self):
        stime= datetime.strptime(self.sunTime, "%H:%M")
        stime=stime+timedelta(minutes=1)
        self.sunTime=stime.strftime("%H:%M")
    def increaseMoonTime(self):
        mtime= datetime.strptime(self.moonTime, "%H:%M")
        mtime=mtime+timedelta(minutes=1)
        self.moonTime=mtime.strftime("%H:%M")
    def decreaseSunTime(self):
        stime= datetime.strptime(self.sunTime, "%H:%M")
        stime=stime-timedelta(minutes=1)
        self.sunTime=stime.strftime("%H:%M")
    def decreaseMoonTime(self):
        mtime= datetime.strptime(self.moonTime, "%H:%M")
        mtime=mtime-timedelta(minutes=1)
        self.moonTime=mtime.strftime("%H:%M")    
        
        # datetime.strptime(params[0], "%Y-%m-%d %H:%M:%S")
    def dayNightSaveTemperature(self):
        if(self.moonSun=='sun'):
            self.desiredSunT=self.desiredT
        else:
            self.desiredMoonT=self.desiredT
    
    def dayNightLoadTemperature(self):

        if(self.moonSun=='sun'):
            self.desiredT=self.desiredSunT
        else:
            self.desiredT=self.desiredMoonT
        self.resetSaveHeater()
        self.refreshDesiredConf=True
        
    def diffTemperature(self):
        return (self.temp-self.desiredT)       
    def getData(self):
        data = {
                'power': self.power,
                'temp': self.temp,
                'temp_desired': self.desiredT,
                'relativeHumidity': self.humidity
            }
        return self.started
    def startHeater(self):
        now = datetime.now()
        #Si se baja la temperatura
        if((self.desiredT > self.temp) and self.power==True):
            #Turn on
            if (self.onTimer<=datetime.now()):
                self.started=True
                self.offTimer=datetime.now()+timedelta(minutes=self.offTime)
            self.tAchieved=False

        elif((self.desiredT == self.temp) and self.power==True):
            self.tAchieved=True
            #Turn off       
            if(self.offTimer<=datetime.now()):
                self.started=False
                self.onTimer=datetime.now()+timedelta(minutes=self.onTime)
        elif(self.power==True):
            self.tAchieved=False    
            if(self.offTimer<=datetime.now()):
                self.started=False
                self.onTimer=datetime.now()+timedelta(minutes=self.onTime)          
        elif(self.power==False):
            self.started=False
            self.tAchieved=False
            self.resetSaveHeater()
        self.refreshDesiredConf=True    
        return self.onOff()
    
    def onOff(self):
        if(ts.started and ts.errors==False and ts.power):
            return True
        else:
            return False
    
    def powerP(self):
        if(self.power==True):
            self.power=False
        else:
            self.resetSaveHeater()
            self.power=True
        self.refreshDesiredConf=True
    def resetSaveHeater(self):
        self.onTimer=datetime.now()
        self.offTimer=datetime.now()

    def changeDayNight(self):
        now=datetime.now().strftime("%H:%M")
        if(now==self.sunTime and self.moonSun=='moon' ):
            self.moonSun='sun'
            self.dayNightLoadTemperature()           
        elif(now==self.moonTime and self.moonSun=='sun'):
            self.moonSun='moon'
            self.dayNightLoadTemperature()
ts=ThermostatService(True)