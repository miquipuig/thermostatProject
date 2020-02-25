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
import threading
import time as time
import os, sys
from .screenUtilites import su
from .dataService import ts
from .import *  
class ScreenLoopButton:
    def __init__(self,canvas,mainImage,pressedImage,width,height,posx, posy,anchor,function,state): 
        self.function=function
        # self.pathname = os.path.dirname(sys.argv[0])
        # self.fullpath = os.path.abspath(self.pathname)  
        self.state=True 
        self.canvas=canvas
        self.active=True
        self.imageState1=su.resizeImgTk(PATHNAME+IMG_PATH+mainImage,width,height)
        self.imageState2=su.resizeImgTk(PATHNAME+IMG_PATH+pressedImage,width,height) 
        self.button=self.canvas.create_image(posx,posy,image=imageState1, anchor=anchor)        
        self.canvas.tag_bind(self.button, '<Button-1>', self.actionPress)

    
    def actionPress(self,event):
        if(self.state):
            self.state=False
            self.canvas.itemconfig(self.button, image = self.imageState2)
        else:
            self.state=True
            self.canvas.itemconfig(self.button, image = self.imageState1)
        self.function()
   
    def hide(self):
        self.canvas(self.button, state='hidden')