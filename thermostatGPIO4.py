# import Adafruit_DHT
# import RPi.GPIO as GPIO
import threading
import numpy as np
import time
from datetime import datetime
from thermostatService import ts
import random
# sensor = Adafruit_DHT.DHT22
pin = 26


class ThermostatGPIO():
  
    
    temperature=np.ones(7)*20
    humidity=np.ones(7)*50


    
    def callback_init(self):
        print('callback init')
        # Corrriente pin 13

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

            t=random.gauss(20,4)
            h=random.gauss(50,5)
            # h, t = Adafruit_DHT.read_retry(sensor, pin)
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
                
               
        
            else:
                print("Failed to get data from sensor.") 
                ts.errors=True
            
                  
            
            # except Exception as ex:
            #     print(ex)
            #     print('salgo aqui')
            #     ts.errors=True
            #     GPIO.output(13,GPIO.LOW)
                
            time.sleep(interval)
    
    def saveloop(self,interval):
        upState=True
        while True:
            # More statements comes here

            #Refresh pin
            try:
                if (ts.onOff() and upState):
                        # GPIO.output(13,GPIO.HIGH)
                        upState=False
                elif(ts.started==False or ts.errors or ts.power==False):
                    # GPIO.output(13,GPIO.LOW)
                    upState=True
            
            except Exception as ex:
                print(ex)
                # GPIO.output(13,GPIO.LOW)
                ts.errors=True

                
            time.sleep(interval)

tg=ThermostatGPIO()