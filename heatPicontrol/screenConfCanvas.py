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
try:
    import tkinter as tk
    import tkinter.font as tkFont
    from tkinter import *
    from tkinter.ttk import *

except ImportError:
    from Tkinter import *
    import Tkinter as tk
    import tkFont
from PIL import Image, ImageTk, ImageSequence
import os, sys
from .screenLoopButton import ScreenLoopButton
from .screenUtilites import su
from .dataService import ts
from . import *  
class ScreenConfCanvas:
    def __init__(self,parent,canvas):
        self.pathname = os.path.dirname(sys.argv[0])
        self.fullpath = os.path.abspath(self.pathname)  
        self.parent=parent
        self.active=True   
        
        self.confCanvas=Canvas(parent, width=380, height=240, bg='white', bd=0, highlightthickness=0, relief='ridge')
        self.fnt1 = tkFont.Font(family='Digital dream Narrow', size=20 , weight='normal')
        self.fnt2 = tkFont.Font(family='Digital dream Narrow', size=10 , weight='normal')
        
        
        self.timeUpSun=ScreenLoopButton(self.confCanvas, 'arrow_up02.png','arrow_up03.png',60, 60, 160,40,'center',self.sunTimeUp)
        self.timeDownSun=ScreenLoopButton(self.confCanvas, 'arrow_down02.png','arrow_down03.png',60, 60, 160,90,'center',self.sunTimeDown)
        self.sunTime=self.confCanvas.create_text(45 ,65,fill='black',font=self.fnt1,text=ts.sunTime, tag='time',anchor='w')
        self.sun=su.resizeImgTk(PATHNAME+IMG_PATH+'sun2.png',60,60)
        self.sunImage=self.confCanvas.create_image(10,40,image=self.sun, anchor='center')
        self.sunTemp=self.confCanvas.create_text(45 ,90,fill='black',font=self.fnt2,text=str(ts.desiredSunT)+'º',tag='ip',anchor='w')
        
        self.timeUpMoon=ScreenLoopButton(self.confCanvas, 'arrow_up02.png','arrow_up03.png',60, 60, 160,150,'center',self.moonTimeUp)
        self.timeDownMoon=ScreenLoopButton(self.confCanvas, 'arrow_down02.png','arrow_down03.png',60, 60, 160,200,'center',self.moonTimeDown)
        self.moonTime=self.confCanvas.create_text(45 ,175,fill='black',font=self.fnt1,text=ts.moonTime, tag='time',anchor='w')
        self.moon=su.resizeImgTk(PATHNAME+IMG_PATH+'moon3.png',85,85)
        self.moonImage=self.confCanvas.create_image(15,160,image=self.moon, anchor='center')
        self.moonTemp=self.confCanvas.create_text(45 ,200,fill='black',font=self.fnt2,text=str(ts.desiredMoonT)+'º',tag='ip',anchor='w')
                  
       
        self.restartButton=ScreenLoopButton(self.confCanvas, 'red-button01.png','red-button-p01.png',50, 50, 330,40,'center',self.errorSet,False)
        self.ipText=self.confCanvas.create_text(300 ,40,fill='black',font=self.fnt2,text='Restart',tag='ip',anchor='e')
       
        #IP connection
        self.wifi=su.resizeImgTk(PATHNAME+IMG_PATH+'wifi01.png',18,20)
        self.wifiImage=self.confCanvas.create_image(360,222,image=self.wifi, anchor='center')   
        self.ipText=self.confCanvas.create_text(345 ,230,fill='black',font=self.fnt2,text=ts.ip,tag='ip',anchor='e')
        
        self.wifiE=su.resizeImgTk(PATHNAME+IMG_PATH+'internet01.png',18,20)
        self.wifiImageE=self.confCanvas.create_image(360,197,image=self.wifiE, anchor='center')   
        self.ip_externalText=self.confCanvas.create_text(345 ,205,fill='black',font=self.fnt2,text=ts.ip_external,tag='ip',anchor='e')
        #FRAME
        self.confCanvas.create_rectangle(0, 0, 380, 240, outline=tgreen, width=10)
        self.confCanvas.create_rectangle(5, 5, 375, 235, outline='grey', width=2)
        self.show()
    def hide(self):
        self.confCanvas.place_forget() 
    def show(self):
        self.confCanvas.place(relx=0.5, rely=0.51,anchor=tk.CENTER)
    def delete(self):
        self.confCanvas.delete("all")
    def showHide(self):
        if(self.active==True):
            self.active=False
            self.hide()
        else:
            self.active=True
            self.show()
    def functionA(self):
        ts.decreaseTemperature()
    
    def sunTimeUp(self):
        ts.increaseSunTime()
        self.confCanvas.itemconfig(self.sunTime,text=ts.sunTime)     
    def sunTimeDown(self):
        ts.decreaseSunTime()
        self.confCanvas.itemconfig(self.sunTime,text=ts.sunTime)  
    def moonTimeUp(self):
        ts.increaseMoonTime()
        self.confCanvas.itemconfig(self.moonTime,text=ts.moonTime)  
    def moonTimeDown(self):
        ts.decreaseMoonTime()
        self.confCanvas.itemconfig(self.moonTime,text=ts.moonTime)  
    def refreshData(self):
        self.confCanvas.itemconfig(self.ipText,text=ts.ip, anchor='e')
        self.confCanvas.itemconfig(self.ip_externalText,text=ts.ip_external, anchor='e')
        self.confCanvas.itemconfig(self.sunTemp,text=str(ts.desiredSunT)+'º')
        self.confCanvas.itemconfig(self.moonTemp,text=str(ts.desiredMoonT)+'º')
    def errorSet(self):
        ts.errors=True
        os.system('shutdown -r now')