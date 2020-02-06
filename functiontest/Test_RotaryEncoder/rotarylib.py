#!/usr/bin/env python3
from tkinter import *
import tkinter as tk
from tkinter.font import Font
from tkinter import messagebox
import math,cmath

class draw_it(tk.Frame):    
    def __init__(self, parent,
                 max_value: (float, int)=100.0,
                 min_value: (float, int)= 0.0,
                 sizeh: (float, int)=100,
                 sizew: (float, int)=100,
                 bg_col:str='blue',
                 unit: str=None,
                 **options):
        tk.Frame.__init__(self, parent, **options)
        self.sizeh = sizeh
        self.sizew = sizew
        self.max_value = float(max_value)
        self.min_value = float(min_value)
        self.bg_col = bg_col
        self.unit = '' if not unit else unit
        
        self.canvas = tk.Canvas(self, width=self.sizew, height=self.sizeh,bg=bg_col,highlightthickness=0)
        self.canvas.grid(row=0,column=0,stick='news')
        self.xy = [(self.sizew/2, 2*self.sizeh/20), (self.sizew/2+self.sizew/20, self.sizeh/2), (self.sizew/2, self.sizeh/2+self.sizeh/20), (self.sizew/2-self.sizew/20, self.sizeh/2)]
        self.polygon_item = self.canvas.create_polygon(self.xy,fill='white')
 
        self.canvas.create_arc(self.sizew/20, self.sizeh/20, 19.0*self.sizew/20.0, 19.0*self.sizeh/20.0,style="arc",width=self.sizeh/10,start=0, extent=60,
                       outline = "red2",tags=('arc1','arc2'))#style=tk.PIESLICE
        self.canvas.create_arc(self.sizew/20, self.sizeh/20, 19.0*self.sizew/20.0, 19.0*self.sizeh/20.0,width=self.sizeh/10,style="arc",start=60, extent=60,
                       outline = "orange",tags=('arc1','arc2'))
        self.canvas.create_arc(self.sizew/20, self.sizeh/20, 19.0*self.sizew/20.0, 19.0*self.sizeh/20.0,style="arc",width=self.sizeh/10,start=120, extent=60,
                       outline = "green",tags=('arc1','arc2'))#style=tk.PIESLICE
        self.canvas.create_arc(self.sizew/20, self.sizeh/20, 19.0*self.sizew/20.0, 19.0*self.sizeh/20.0,style="arc",width=self.sizeh/10,start=180, extent=60,
                       outline = "yellow",tags=('arc1','arc2'))#style=tk.PIESLICE
        self.canvas.create_arc(self.sizew/20, self.sizeh/20, 19.0*self.sizew/20.0, 19.0*self.sizeh/20.0,style="arc",width=self.sizeh/10,start=240, extent=60,
                       outline = "blue",tags=('arc1','arc2'))#style=tk.PIESLICE
        self.canvas.create_arc(self.sizew/20, self.sizeh/20, 19.0*self.sizew/20.0, 19.0*self.sizeh/20.0,style="arc",width=self.sizeh/10,start=300, extent=60,
                       outline = "white",tags=('arc1','arc2'))#style=tk.PIESLICE
        self.canvas.create_oval(9*self.sizew/20,9* self.sizeh/20, 11*self.sizeh/20.0, 11*self.sizew/20.0,fill="blue",outline="#DDD",width=2)
        self.readout = self.canvas.create_text(self.sizew/2,self.sizeh/4, font=("Arial",int(self.sizew/10),'bold'),fill="light blue", text='0'+self.unit)
        self.canvas.create_text(self.sizew/2,3*self.sizeh/4, font=("Arial",int(self.sizew/15),'bold'),fill="white", text='Ardiotech')
        self.center = self.sizew/2, self.sizeh/2
        
        
    def setangle(self,angle):
        
        cangle = cmath.exp(angle*1j*math.pi/180)
        offset = complex(self.center[0], self.center[1])
        newxy = []
        for x, y in self.xy:
            v = cangle * (complex(x, y) - offset) + offset
            newxy.append(v.real)
            newxy.append(v.imag)
        self.canvas.coords(self.polygon_item, *newxy)
        self.canvas.delete(self.readout)
        label = str(int(angle))
        self.readout = self.canvas.create_text(self.sizew/2,self.sizeh/4, font=("Arial",int(self.sizew/10),'bold'),fill="light blue", text=label+self.unit)

        