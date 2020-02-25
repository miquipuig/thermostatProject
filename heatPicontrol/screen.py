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

import sys
if sys.version_info[0] < 3:
    PVERSION=2
else:
    PVERSION=3

# import tkinter
try:
    import tkinter as tk
    import tkinter.font as tkFont
    from tkinter import *
    from tkinter.ttk import *

except ImportError:
    from Tkinter import *
    import Tkinter as tk
    import tkFont

import time as time
import datetime
import threading
#images
import os, sys
from .dataService import ts
from .screenUtilites import su
from .screenDiagram import ScreenDiagram
from.screenConfCanvas import ScreenConfCanvas
from .import *

iteration=False

class ThermostatScreen:
 
    def __init__(self):
        
        self.root = tk.Tk()
        
        
        if(env=='production'):
            self.root.attributes("-fullscreen", True)
            self.root.config(cursor='none')
        self.root.wm_attributes("-topmost", True)
        self.root.wm_attributes("-alpha", True)
        self.root.configure(background=bg)
        self.root.geometry("480x320") #Width x Height
        self.root.bind("<Escape>", quit)
        self.root.bind("x", quit)
        self.run(self.root)
        
    def mainloop(self):
        self.root.mainloop()
  
    def run(self, parent):

        if(PVERSION==2):
            self.gradeSymbol = u'\u00BA'
            self.gradeSymbol = self.gradeSymbol.encode('utf-8')
        else:
            self.gradeSymbol = '\u00BA'
        self.iteration=False
        #-------------    
        #   BUTTONS
        #-------------
        self.fnt1 = tkFont.Font(family='Digital-7 Mono', size=25, weight='normal')
        self.fnt1 = tkFont.Font(family='Digital-7 Mono', size=20 , weight='normal')
        self.fnt2 = tkFont.Font( family='Garden Grown US', size=125, weight='normal')
        self.fnt3 = tkFont.Font( family='Arial', size=70, weight='bold')
        self.fnt4 = tkFont.Font( family='Calibri', size=20, weight='bold')      

        colorSymbolButton= tblue
        colorButton=bg
        self.style = Style() 
        self.style.configure('TButton', font = ('calibri', 20, 'bold'), borderwidth = '0')
        self.style.map('TButton', foreground = [('!disabled','!disabled','black')], background =[('!disabled',tblue)])
               
        #Hora y temperatura ambiente
        self.horaText = tk.StringVar()
        self.txt3 = tk.StringVar()
        self.horaText.set(time.strftime('%-I:%M:%S %p'))
        self.txt3.set("{0:0.0f}{1}C {2:0.1f}%".format(ts.temp,self.gradeSymbol,ts.humidity ))
        self.lecturesLabel = tk.Label(parent, textvariable=self.txt3, font=self.fnt1, foreground="white", background=bg, pady = 10)
        self.lecturesLabel.place(relx=0.03, rely=0.93, anchor=tk.W)
        self.horaLabel = tk.Label(parent, textvariable=self.horaText, font=self.fnt1, foreground="white", background=bg, pady = 10)
        self.horaLabel.place(relx=0.82, rely=0.93,anchor=tk.CENTER)
        
        #   Images
        self.pathname = os.path.dirname(sys.argv[0])
        self.fullpath = os.path.abspath(self.pathname)       
        self.weather=su.resizeImgTk(self.fullpath+IMG_WEATHER_PATH+ts.weatherIcon+'.png',80,80)
        self.moon= su.resizeImgTk(self.fullpath+IMG_PATH+'moon3.png',100,100)
        self.sun=su.resizeImgTk(self.fullpath+IMG_PATH+'sun2.png',60,60)
        self.eco=su.resizeImgTk(self.fullpath+IMG_PATH+'eco1.png',70,70)  
        # self.powerUp=su.coloringImgTk(self.fullpath+IMG_PATH+'power7.png',50,50,255,241,169)
        # self.powerDown=su.coloringImgTk(self.fullpath+IMG_PATH+'power7.png',50,50,169, 183, 255)
        self.powerUp=su.resizeImgTk(self.fullpath+IMG_PATH+'poweroff02.png',50,50)
        self.powerDown=su.resizeImgTk(self.fullpath+IMG_PATH+'poweron02.png',50,50)
        # self.wifi=su.coloringImgTk(self.fullpath+IMG_PATH+'wifi01.png',30,30,169, 183, 255)
        self.wifi=su.resizeImgTk(self.fullpath+IMG_PATH+'wifi04.png',25,25)
        self.nowifi=su.resizeImgTk(self.fullpath+IMG_PATH+'wifi_error04.png',25,25)
        self.error=su.resizeImgTk(self.fullpath+IMG_PATH+'error01.png',25,25)
        self.alarm=su.resizeImgTk(self.fullpath+IMG_PATH+'alarmConf01.png',30,30)
        

        #BOTTOM CANVAS
        self.canvas = Canvas(parent, width=480, height=280, bg=bg, bd=0, highlightthickness=0, relief='ridge')
        self.canvas.place(relx=1, rely=0,anchor=tk.NE)    

        self.flameIndex=0
        self.flameState=0
        self.flames0 = su.animatedGifTk(self.fullpath+IMG_PATH+'flame13.gif', {'width':500})
        self.flames1 = su.animatedGifTk(self.fullpath+IMG_PATH+'flame15.gif', {'width':480,'height':180 })
        self.flames2 = su.animatedGifTk(self.fullpath+IMG_PATH+'flame03.gif', {'width':64})
        self.flames=self.flames0
        self.flameGif=self.canvas.create_image(240, 260, image=self.flames[0],anchor='s')
       
        self.wifiIcon=self.canvas.create_image(380,25,image=self.nowifi)


        #WEATHER INFO
        self.weatherIcon=self.canvas.create_image(170,35, image=self.weather, tag='weather')
        self.weatherText=self.canvas.create_text(200,30,fill=twhite,font=self.fnt1,text=str(ts.weatherTemp) + 'º ' + str(ts.weatherHumidity)+'%', tag='weather',anchor='w')
        #ECO ICON
        self.ecoImage=self.canvas.create_image(335, 80, image=self.eco)    
      
        #SELECTED TEMPERATURE
        self.tempText3=self.canvas.create_text(320,155,fill=twhite,font=self.fnt2, text="º", anchor='w')
        self.tempText2=self.canvas.create_text(260,155,fill=twhite,font=self.fnt2, text="%0.0f" % (ts.desiredT%1*10 ), anchor='w')
        self.tempText1=self.canvas.create_text(255,155,fill=twhite,font=self.fnt2, text="%i." % (ts.desiredT), anchor='e')
        
        #PLUS/MINUS BUTTON
        self.minusButton=self.canvas.create_text(118,130,fill=tblue,font=self.fnt3, text="-")
        self.plusButton=self.canvas.create_text(350,135,fill=tblue,font=self.fnt3, text="+")  
        self.canvas.tag_bind(self.minusButton, '<Button-1>', self.restaD)
        self.canvas.tag_bind(self.minusButton, '<ButtonRelease-1>', self.restaU)
        self.canvas.tag_bind(self.plusButton, '<Button-1>', self.sumaD)
        self.canvas.tag_bind(self.plusButton, '<ButtonRelease-1>', self.sumaU)
       
        # DATA DIAGRAM
        self.diagram=ScreenDiagram(parent,self.canvas)
        
        #CONFIGURATION DAY NIGHT BUTTON
        self.alarmButton=self.canvas.create_image(450, 85, image=self.alarm)
        self.canvas.tag_bind(self.alarmButton, '<ButtonRelease-1>', self.alarmClick)
        

        # CONFIGURATION CANVAS
        self.confCanvas = ScreenConfCanvas(parent,self.canvas)  
    
       
        #TIME & LECTURES
        # self.timeText=self.canvas.create_text(475,300,fill=twhite,font=self.fnt1,text=time.strftime('%-I:%M:%S %p'), tag='time',anchor='e')
        # self.lecturesText=self.canvas.create_text(5,300,fill=twhite,font=self.fnt1,text="{0:0.0f}{1}C {2:0.1f}%".format(ts.temp,self.gradeSymbol,ts.humidity), tag='time',anchor='w')
        #POWER BUTTON
        if (ts.power==True):
            self.power=self.canvas.create_image(40, 35, image=self.powerUp)
        else:
            self.power=self.canvas.create_image(40, 35, image=self.powerDown)
        self.canvas.tag_bind(self.power, '<ButtonPress-1>', self.powerClick)
        #MOON SOON BUTTON
        self.sunMoonIcon=self.canvas.create_image(440, 35, image=self.sun)
        self.canvas.tag_bind(self.sunMoonIcon, '<ButtonPress-1>', self.moonSunClick)
        
        #ERROR ICON
        self.errorIcon=self.canvas.create_image(350,25,image=self.error)
        self.errorSquare=self.canvas.create_rectangle(0, 0, 480, 0, outline=tred , width=10)
        
        self.canvas.tag_bind(self.flameGif, '<ButtonPress-1>', self.flameClick)
        
        self.canvas.bind("<Button-1>", self.canvasClick)
        t = threading.Thread(target=self.animatedFrame, args=())
        t.daemon = True
        t.start()

       
       
        
        self.delayCount1=100
        self.delayCount2=100
        self.delayCount3=100
        self.canvas.after(500, self.refresh_canvas)   
        
        # self.up=ScreenButton(self.canvas)
    def animatedFrame(self):
        while(True):    
            self.flameIndex+=1
            if(self.flameIndex>=len(self.flames)):
                self.flameIndex=0
            self.canvas.itemconfig(self.flameGif, image=self.flames[self.flameIndex])
            time.sleep(0.03)
    
    def alarmClick(self,event):

        self.confCanvas.showHide()
    def canvasClick(self,event):
        self.confCanvas.hide()
    def moonSunClick(self, event):
        if(ts.moonSun=='sun'):
            ts.moonSun='moon'
            self.canvas.itemconfig(self.sunMoonIcon, image = self.moon)
        else:
            ts.moonSun='sun' 
            self.canvas.itemconfig(self.sunMoonIcon, image = self.sun)
        ts.dayNightLoadTemperature()
        self.refresh_tempLabel()
        
    def flameClick(self, event): 
        if(self.flameState<2):
            self.flameState+=1
        else:
            self.flameState=0
        if(self.flameState==0):
            self.flameIndex=0
            self.flames=self.flames0
            self.canvas.coords(self.flameGif,225,260)
        elif(self.flameState==1):
            self.flameIndex=0
            self.flames=self.flames1
            self.canvas.coords(self.flameGif,240,200) 
        elif(self.flameState==2):
            self.flameIndex=0
            self.flames=self.flames2
            self.canvas.coords(self.flameGif,40,190) 
        
    def refreshFlameState(self):
        
        if(ts.onOff()):
            self.canvas.itemconfig(self.flameGif, state='normal')
        else:
            self.canvas.itemconfig(self.flameGif, state='hidden')
    
    def refreshEcoState(self):
        if(ts.ecoState()):
            self.canvas.itemconfig(self.ecoImage, state = 'normal')
            self.canvas.itemconfig(self.tempText3, state = 'hidden')

        else:           
            self.canvas.itemconfig(self.ecoImage, state = 'hidden')
            self.canvas.itemconfig(self.tempText3, state = 'normal')   
        
    def quit(self):
        root.destroy()
    def powerClick(self, event):
        ts.powerP()
        if (ts.power==True):
            self.canvas.itemconfig(self.power, image = self.powerUp)
        else:
            self.canvas.itemconfig(self.power, image = self.powerDown)
        
    def refresh_tempLabel(self):
        # self.tempLabel.configure(text="%s%sC" % (str(np.around(ts.desiredT, decimals=1)) , self.gradeSymbol))
        # self.tempLabel.configure(text="%0.1f%s" % (ts.desiredT , self.gradeSymbol))
        self.canvas.itemconfig(self.tempText2,text="%0.0f" % (ts.desiredT%1*10))
        self.canvas.itemconfig(self.tempText1,text="%i." % (ts.desiredT))
        
    def refresh_sunMoon(self):
  
        if(ts.moonSun=='sun'):
            self.canvas.itemconfig(self.sunMoonIcon, image = self.sun)
        else:
            self.canvas.itemconfig(self.sunMoonIcon, image = self.moon)
       
    def refresh_tempLabel_full(self):
        ts.startHeater()
        self.refresh_tempLabel()
        self.refresh_sunMoon()
        self.confCanvas.refreshData()
        if (ts.tAchieved and ts.power):
            self.canvas.itemconfig(self.tempText3,fill=tgreen)
            self.canvas.itemconfig(self.tempText2,fill=tgreen)
            self.canvas.itemconfig(self.tempText1,fill=tgreen)
        else:
            self.canvas.itemconfig(self.tempText3,fill='white')
            self.canvas.itemconfig(self.tempText2,fill='white')
            self.canvas.itemconfig(self.tempText1,fill='white')
        ts.refreshDesiredConf=False
        self.refreshEcoState()
        self.refreshFlameState()
    
    def sumaW(self):
        sleepTime=0.400
        while(self.iteration==True):
            ts.increaseTemperature()
            time.sleep(sleepTime)
            sleepTime-=(sleepTime/10)
        # ts.startHeater()
    def restaW(self):
        sleepTime=0.400
        while(self.iteration==True):
            ts.decreaseTemperature()
            time.sleep(sleepTime)
            sleepTime-=(sleepTime/12)
        # ts.startHeater()
    def sumaD(self,event):
        self.iteration=True
        t = threading.Thread(target=self.sumaW, args=())
        t.daemon = True
        t.start()
    def sumaU(self,event):
        self.iteration=False
        
    def restaU(self,event):
        self.iteration=False
    def restaD(self,event):
        self.iteration=True
        t = threading.Thread(target=self.restaW, args=())
        t.daemon = True
        t.start()
        
    def refreshWifi(self):
        if(ts.online):
            self.canvas.itemconfig(self.wifiIcon,image=self.wifi)
        else:
            self.canvas.itemconfig(self.wifiIcon,image=self.nowifi)
    def refreshErrors(self):
        if(ts.errors):
            self.canvas.itemconfig(self.errorIcon,state='normal')
            self.canvas.itemconfig(self.errorSquare,state='normal')
        else:
            self.canvas.itemconfig(self.errorIcon,state='hidden')
            self.canvas.itemconfig(self.errorSquare,state='hidden')
    def refresh_canvas(self):
        self.horaText.set(time.strftime('%-I:%M:%S %p')) 
        self.refreshErrors()       
        if(ts.refreshDataListener):
            #Refresh Lectures        
            self.txt3.set("{0:0.1f}{1}C {2:0.1f}%".format(ts.temp,self.gradeSymbol,ts.humidity))
            ts.refreshDesiredConf=True           
            #Refresh weather state and wifi
            if(self.delayCount2>3):
                self.delayCount2=0
                self.weather=su.resizeImgTk(self.fullpath+IMG_WEATHER_PATH+ts.weatherIcon+'.png',80,80)
                self.canvas.itemconfig(self.weatherIcon, image = self.weather)
                self.canvas.itemconfig(self.weatherText,text=str(ts.weatherTemp) + 'º ' + str(ts.weatherHumidity)+'%')     
                self.refreshWifi()
            #Refresh Diagram
            if(self.delayCount3>0):
                self.delayCount3=0
                self.diagram.refreshData()
            self.delayCount1+=1
            self.delayCount2+=1
            self.delayCount3+=1
            ts.refreshDataListener=False

        if(ts.refreshDesiredConf):
            ts.refreshDesiredConf=False
            self.refresh_tempLabel_full()
        
        self.canvas.after(300, self.refresh_canvas)