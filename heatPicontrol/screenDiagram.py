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

from PIL import Image, ImageTk, ImageSequence

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
import numpy as np
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
from matplotlib.dates import DateFormatter
import matplotlib.pyplot as plt
#lineCollection
from matplotlib.collections import LineCollection
from matplotlib.colors import ListedColormap, BoundaryNorm
from .dataService import ts
from .screenUtilites import su
from .import *

   
class ScreenDiagram:
    def __init__(self,parent,canvas):
   
        self.parent=parent
        self.canvas=canvas
        self.active=True
        self.graph='T'
        self.canvasFigure=None  
        self.fig, self.ax = plt.subplots()        
        # fig.patch.set_alpha(0.5)
        #Diagram Size
        self.fig.set_size_inches(5, 0.87)
        self.fig.subplots_adjust(top=0.85) #adjust plot inside
        self.fig.subplots_adjust(bottom=0.02) #adjust plot inside
        self.fig.subplots_adjust(left=0.08) #adjust plot inside
        # self.fig.subplots_adjust(right=1.095) #adjust plot inside
        self.fig.subplots_adjust(right=0.9) #adjust plot inside
        self.fig.subplots_adjust(hspace=0) #adjust plot inside
        self.fig.patch.set_facecolor(bg) #color figura
        
        self.__createCanvas()
        
        
        
        #It need a semaphore like a atomic function -  concurrency problems
        # x=ts.th.extractHistoricData(0)
        # y=ts.th.extractHistoricData(1)
        # z=ts.th.extractHistoricData(2)
        self.date_form = DateFormatter("%H:%M")
        
        data=ts.th.extractHistoricData([0,1,2])
        x=data[0]
        y=data[1]
        z=data[2]
        
        # x = [datetime.datetime.now() + datetime.timedelta(hours=i) for i in range(12)]
        # y = [i+random.gauss(0,1) for i,_ in enumerate(x)]
        self.ax.plot(x,y,linewidth=2)
        self.ax.plot(x,z)
        
        # x = np.arange(100)
        # y = 10*np.sin(x / 50) +13
        # points = np.array([x, y]).T.reshape(-1, 1, 2)
        # segments = np.concatenate([points[:-1], points[1:]], axis=1)
        # norm = plt.Normalize(y.min(), y.max())
        # lc = LineCollection(segments, cmap='viridis', norm=norm)
        # lc.set_array(y)
        # lc.set_linewidth(2)
        # line = self.ax.add_collection(lc)
        
        # self.ax.set_xlim(x.min(), x.max()) #rango en x
        # self.ax.set_ylim(y.min(),y.max() +1 ) #rango en y
        # # ax.step(x, y + 2, 'red', label='pre (default)')
        # self.ax.plot(x, y -0.1*x, color='green', alpha=0.5)
        # ax.plot(x, y + 2,'C0o', color='red', alpha=0.5)
        # ax.step(x, y + 1, where='mid', label='mid')
        # ax.plot(x, y + 1, 'C1o', alpha=0.5)

        # ax.step(x, y, where='post', label='post')
        # ax.plot(x, y, 'C2o', alpha=0.5)
 
        #colors and borderse
        self.ax.set_facecolor(bg)     
        self.ax.axis('on') #border
        self.ax.spines['top'].set_color(bg)
        self.ax.spines['left'].set_color(bg)
        self.ax.spines['bottom'].set_color(bg)
        self.ax.spines['right'].set_color(bg)
        #xaxis conf
        self.ax.tick_params(axis='x', colors=tblue, labelsize=7, direction="in", pad= 1)
        
        self.ax.xaxis.tick_top()
        # ax.xaxis.get_major_ticks()
        #yaxis conf
        self.ax.yaxis.label.set_color(tblue)
        self.ax.tick_params(axis='y', colors=tblue, labelsize=7, direction="in", pad=2.5)
        # #colorbar config
        # cbar=self.fig.colorbar(line, ax=self.ax)
        # cbar.outline.set_edgecolor(bg)
        # cbar.ax.yaxis.set_tick_params(color=tblue, labelsize=7, direction="in", pad= 2)
        # cbytick_obj = plt.getp(cbar.ax.axes, 'yticklabels')
        # plt.setp(cbytick_obj, color=tblue)    
        # self.fig.patch.set_visible(True)    
        # #ax.legend(title='Parameter where:') #legend
        
        
        #DIAGRAM BUTTONS
        
        self.humidityImage=su.resizeImgTk(PATHNAME+IMG_PATH+'humidityico02.png',35,35)
        self.termoImage=su.resizeImgTk(PATHNAME+IMG_PATH+'termoico02.png',35,35)
        self.digramButton=self.canvas.create_image(450, 180, image=self.termoImage)
        self.canvas.tag_bind(self.digramButton, '<Button-1>', self.canvasClick)
        
    def refreshData(self):
        if(self.active):
            if(self.graph=='T'):
                data=ts.th.extractHistoricData([0,1,2])
            elif(self.graph=='H'):
                data=ts.th.extractHistoricData([0,3,4])
            x=data[0]
            y=data[1]
            z=data[2]
            try:
                self.ax.clear()
                self.ax.xaxis.set_major_formatter(self.date_form)
                self.ax.plot(x,y,linewidth=3)
                self.ax.plot(x,z)
                self.fig.canvas.draw_idle()
            except Exception as ex:
                logger.error(ex)
    
    def destroy(self):
        self.active=False
        self.canvasFigure.get_tk_widget().destroy()
        
    def canvasClick(self,event):
        if(self.graph=='T'):
            self.graph='H'
            self.canvas.itemconfig(self.digramButton, image = self.humidityImage)
        elif(self.graph=='H'):
            self.graph='T'
            self.canvas.itemconfig(self.digramButton, image = self.termoImage)
        self.refreshData()
    def reconstruct(self):
        self.active=True
        self.__createCanvas()
    
    def __createCanvas(self):
        self.canvasFigure = FigureCanvasTkAgg(self.fig, master=self.parent)  # A tk.DrawingArea.
        self.canvasFigure.draw_idle()
        self.canvasFigure.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=2)
        self.canvasFigure.get_tk_widget().place(relx=0.5, rely=0.625,anchor=tk.N)
        self.canvasFigure.callbacks.connect('button_press_event', self.canvasClick)
        
