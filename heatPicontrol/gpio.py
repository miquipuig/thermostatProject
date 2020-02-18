
import RPi.GPIO as GPIO
import threading
import numpy as np
import Adafruit_DHT
import RPi.GPIO as GPIO
import time
from datetime import datetime
from .dataService import ts
from . import *
import random
sensor = Adafruit_DHT.DHT22
pin = 26 #PIN SENSOR DHT22 - 26


class ThermostatGPIO():
    
    gpioB = 16 #Rotatory sensor - 16 & 12
    gpioA = 12 #Rotatory sensor - 16 & 12
    gpioC = 21
    levA = 0
    levB = 0
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(13,GPIO.OUT) # Relay - 13
    # GPIO.setup(16,GPIO.OUT)
    GPIO.output(13,GPIO.LOW)

    #Rotatory
    GPIO.setup(gpioA, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(gpioB, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    
    temperature=np.ones(7)*20
    humidity=np.ones(7)*50


    
    def callback_init(self):
        GPIO.add_event_detect(self.gpioA, GPIO.BOTH , self._callbackA)
        GPIO.add_event_detect(self.gpioB, GPIO.BOTH , self._callbackA)

    def _callbackA(self,channel):
        level = GPIO.input(channel)
        if channel == self.gpioA:
            self.levA =level
        else:
            self.levB=level
        if channel == self.gpioA and level == 1:
            if self.levB == 1:
                ts.decreaseTemperature()
        elif channel == self.gpioB and level == 1:
            if self.levA == 1:
                ts.increaseTemperature()
        
            
    def readloop(self, interval):
        # global temperatura
        # global humitat
        count=0
        
        while True:
            h, t = Adafruit_DHT.read_retry(sensor, pin)
            if h is not None and t is not None:
                
                
                self.temperature=np.append(self.temperature,t)
                self.temperature=np.delete(self.temperature, 0)
                self.humidity=np.append(self.humidity,h)
                self.humidity=np.delete(self.humidity, 0)
                

                if(count<7):
                    ts.updateHomeClimate(t, h)
                    count+=1
                else:
                    ts.updateHomeClimate(np.median(self.temperature), np.median(self.humidity))
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S")+' - '+"Temp={0:0.2f}*C Humidity={1:0.1f}%".format(t, h)+" Temp_median="+str(np.median(self.temperature)))
                
                # https://api.openweathermap.org/data/2.5/weather?zip=08014,es&appid=35bef01f2be23b616aa0457916b79b5d
                
                if (ts.startHeater()):
                    GPIO.output(13,GPIO.HIGH)
                else:
                    GPIO.output(13,GPIO.LOW)
        
            else:
                print("Failed to get data from sensor.") 
                GPIO.output(13,GPIO.LOW)
                ts.errors=True
            
                  
            
            # except Exception as ex:
            #     print(ex)
            #     print('salgo aqui')
            #     ts.errors=True
            #     GPIO.output(13,GPIO.LOW)
                
            time.sleep(interval)
    
    def saveloop(self, interval):
        upState=True
        while True:
            # More statements comes here

            #Refresh pin
            try:
                if (ts.onOff() and upState):
                        GPIO.output(13,GPIO.HIGH)
                        upState=False
                elif(ts.started==False or ts.errors or ts.power==False):
                    GPIO.output(13,GPIO.LOW)
                    upState=True
            
            except Exception as ex:
                print(ex)
                GPIO.output(13,GPIO.LOW)
                ts.errors=True

                
            time.sleep(interval)

tg=ThermostatGPIO()