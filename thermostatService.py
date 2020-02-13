# current date and time
from datetime import datetime,timedelta
import numpy as np
import random
from thermostatHistory import ThermostatHistory
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
    desiredT = 20.2
    desiredMoonT=18
    desiredSunT=20
    moonSun='sun' #Day or night
    

    #States
    online=True
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
        self.updateWheather()
        self.temp = np.around(temp, decimals=1)
        self.th.historicData.append([datetime.now(),temp,self.desiredT,relativeHumidity])
        self.humidity = relativeHumidity
        self.refreshDataListener=True
        
        if(self.compressCounter<25):
            self.compressCounter+=1
        else:
            self.th.compress()
            self.compressCounter=0
        # self.th.storeData()
        
    def addCallbackFunction(self, function):
        self.tvCallbackFunction=function
    
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
                self.weatherHumidity=np.around(resp_dict['main']['humidity']-273.15,decimals=2)
                self.weatherIcon=json.loads(json.dumps(resp_dict['weather'][0]))['icon']
                self.weatherDesciption=json.loads(json.dumps(resp_dict['weather'][0]))['description']
            except Exception as ex:
                self.online=False
                print(ex)
        self.weatherCounter+=1
        
    def setTemperature(self, temp):
        if(temp<29|temp>9):
            self.desiredT = temp
            self.dayNightSaveTemperature()
            self.refreshDataListener=True
    
    def ecoState(self):
        if(self.moonSun=='sun'):
            if(self.desiredT<22 and self.power):
                return True
        else:
            if(self.desiredT<20 and self.power):
                return True
        return False
                    
    def increaseTemperature(self):
        if(self.desiredT<28):
            self.desiredT =round(self.desiredT + 0.1,1)
            # self.startHeater()
            self.tvCallbackFunction()
            self.refreshDesiredConf=True
            self.dayNightSaveTemperature()
        self.resetSaveHeater()

        
    def decreaseTemperature(self):
        if(self.desiredT>10):
            self.desiredT = round(self.desiredT - 0.1,1)
            # self.startHeater()
            self.tvCallbackFunction()
            self.refreshDesiredConf=True
            self.dayNightSaveTemperature()
        self.resetSaveHeater()
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
        self.startHeater()
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
        # print('desiredT: '+str(self.desiredT) + 'temp: '+str(self.temp))
        if((self.desiredT > self.temp) and self.power==True):
            # print(1)
            #Turn on
            if (self.onTimer<=datetime.now()):
                # print(11)
                self.started=True
                self.offTimer=datetime.now()+timedelta(minutes=self.offTime)
            self.tAchieved=False

        elif((self.desiredT == self.temp) and self.power==True):
            # print(2)
            self.tAchieved=True
            #Turn off       
            if(self.offTimer<=datetime.now()):
                # print(21)
                self.started=False
                self.onTimer=datetime.now()+timedelta(minutes=self.onTime)
        elif(self.power==True):
            # print(3)
            self.tAchieved=False    
            if(self.offTimer<=datetime.now()):
                # print(31)
                self.started=False
                self.onTimer=datetime.now()+timedelta(minutes=self.onTime)          
        elif(self.power==False):
            print(4)
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

ts=ThermostatService(True)