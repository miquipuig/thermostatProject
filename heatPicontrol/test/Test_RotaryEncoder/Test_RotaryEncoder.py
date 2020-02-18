#!/usr/bin/env python3
from tkinter import *
import tkinter as tk
from tkinter.font import Font
from tkinter import messagebox
import time
from time import sleep
import random
import sys
import RPi.GPIO as GPIO
import rotarylib

gpioB = 16 #abans 18
gpioA = 12
counter = 0

GPIO.setmode(GPIO.BCM)
GPIO.setup(gpioA, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(gpioB, GPIO.IN, pull_up_down=GPIO.PUD_UP)


StepPins = [31,35,33,37]
# Set all pins as output
for pin in StepPins:
  GPIO.setup(pin,GPIO.OUT)
  GPIO.output(pin, 0)

Seq = [[1,0,0,1],
       [1,0,0,0],
       [1,1,0,0],
       [0,1,0,0],
       [0,1,1,0],
       [0,0,1,0],
       [0,0,1,1],
       [0,0,0,1]]
       
StepCount = len(Seq)
StepDir =  1# Set to 1 or 2 for clockwise
            # Set to -1 or -2 for anti-clockwise
win = tk.Tk()
a5 = PhotoImage(file="g1.png")
win.tk.call('wm', 'iconphoto', win._w, a5)
win.title("Ardiotech Raspberry Pi Version 2.0")
win.geometry("800x400+0+0")
win.resizable(width=True, height=True)
win.configure(bg='black')
def exitProgram():
 #   if messagebox.askyesno("Print", "Exit?"):
    GPIO.cleanup()
    win.destroy()       
originalPlantImage = tk.PhotoImage(file="g1.png")
image = originalPlantImage.subsample(15, 15)
exitb = tk.Button(win,
        text="Exit",
        image=image,
        font=("Helvetica", 14,'bold'),
        compound="left",
        borderwidth=3,
        width = 60,
        height = 30,              
        bg="lightskyblue",
        fg='black',
        command= exitProgram,
        activebackground="dark gray")
exitb.pack(fill=X,padx=2)
StepCounter=0
def step_it(dir):
    global StepPins,StepCounter,angle
    StepCounter += dir
    if (StepCounter>=StepCount):
        StepCounter = 0
    if (StepCounter<0):
        StepCounter = StepCount+dir
    for pin in range(0, 4):
        xpin = StepPins[pin]
        if Seq[StepCounter][pin]!=0:
          GPIO.output(xpin, True)
        else:
          GPIO.output(xpin, False)
    setRotartAngle(dir)
#    print (dir)


levA = 0
levB = 0

def _callbackA(channel):
    global gpioA,gpioB,levA,levB
    level = GPIO.input(channel)
    if channel == gpioA:
        print('gpioA')
        levA =level
    else:
        print('gpioB')
        levB=level
    if channel == gpioA and level == 1:
        if levB == 1:
            step_it(1)
    elif channel == gpioB and level == 1:
        if levA == 1:
            step_it(-1)
angle=0
p1 = rotarylib.draw_it(
    win,
    max_value=0.0,
    min_value=0.0,
    sizew=300,
    sizeh=300,
    bg_col='black',
    unit = "°")
p1.pack(side=TOP)
g_value =0
def setRotartAngle(dir):
    global g_value
    g_value-=dir*4
    if g_value > 359:
        g_value = 0
    elif g_value < -1:
        g_value = 360
    p1.setangle(int(g_value))
GPIO.add_event_detect(gpioA, GPIO.BOTH , _callbackA)#, bouncetime=10
GPIO.add_event_detect(gpioB, GPIO.BOTH , _callbackA)
# while(True):
#     print(GPIO.input(16))
#     print(GPIO.input(12))
#     print('aaaaaaa')
mainloop()
