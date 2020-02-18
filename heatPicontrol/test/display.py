# import tkinter

try:
    import tkinter as tk
    import tkinter.font as tkFont
    print("Carga librerias Python 3")
    PVERSION=3
except ImportError:
    from Tkinter import *
    import Tkinter as tk
    import tkFont
    print("Carga librerias Python 2")
    PVERSION=2
    
import time
import datetime
import threading
import Adafruit_DHT
import RPi.GPIO as GPIO
# import Adafruit_DHT
# import RPi.GPIO as GPIO

temperatura=0
humitat=0

class Timer:
    def __init__(self, parent):
        
        self.term=21;
        
        if(PVERSION==2):
            self.gradeSymbol = u'\u00BA'
            self.gradeSymbol = self.gradeSymbol.encode('utf-8')
        else:
            self.gradeSymbol = '\u00BA'
        self.fnt = tkFont.Font(family='Georgia', size=28, weight='normal')
        self.fnt2 = tkFont.Font( family='Arial', size=40, weight='bold')
        self.fnt3 = tkFont.Font( family='Arial', size=15, weight='bold')
        self.txt = tk.StringVar()
        self.txt2 = tk.StringVar()
        self.txt3 = tk.StringVar()
        self.txt2.set(time.strftime("%H:%M:%S"))
        
        
        self.txt3.set("{0:0.0f}{1}C {2:0.1f}%".format(temperatura,self.gradeSymbol,humitat ))

        self.lbl = tk.Label(parent, textvariable=self.txt3, font=self.fnt2, foreground="white", background="black")
        self.lbl.place(relx=0.5, rely=0.5, anchor=tk.N)
        self.lbl2 = tk.Label(parent, textvariable=self.txt2, font=self.fnt, foreground="green", background="black")
        self.lbl2.place(relx=0.5, rely=0.50, anchor=tk.S)
        # variable storing time
        self.seconds = 0
        # label displaying time
        #self.label = tk.Label(parent, text="0 s", font="Arial 30", width=10)
        
        self.label = tk.Label(parent, text="21 %sC" % self.gradeSymbol, font="Arial 30", width=10)
        self.label.pack()
        # start the timer
        self.resB = tk.Button(parent, width=1, height=1, text ="-",bd=0,highlightthickness=0, relief=tk.RIDGE,activebackground="red",bg="red",activeforeground="white", fg="white", font = self.fnt, command = self.resta).pack(side=tk.LEFT)
        self.sumB = tk.Button(parent, width=1, height=1, text ="+",bd=0,highlightthickness=0, relief=tk.RIDGE,activebackground="red",bg="red",activeforeground="white", fg="white", font = self.fnt, command = self.suma).pack(side=tk.RIGHT)
        self.shutdown = tk.Button(parent, width=5, height=1, text ="Apagar",bd=0,highlightthickness=0, relief=tk.RIDGE,activebackground="red",bg="red",activeforeground="white", fg="white", font = self.fnt3, command = self.quit).pack(side=tk.BOTTOM)
        self.label.after(1000, self.refresh_label)

    def quit(self):
        root.destroy()

    def refresh_label(self):
        # self.txt2.set(time.strftime("%H:%M:%S"))
        self.txt2.set(time.strftime("%D %H:%M:%S"))
        self.txt3.set("{0:0.0f}{1}C {2:0.1f}%".format(temperatura,self.gradeSymbol,humitat ))
        """ refresh the content of the label every second """
        # increment the time
        #self.seconds += 1
        # display the new time
        #self.label.configure(text="%i s" % self.seconds)
        # request tkinter to call self.refresh after 1s (the delay is given in ms)
        
        
        #COLOR TEMP
        if (self.term>temperatura):
            self.label.configure(background="red")
        elif (self.term<temperatura):
            self.label.configure(background="grey")
        elif (self.term==temperatura):
            self.label.configure(background="green")
        
        self.label.after(1000, self.refresh_label)
        
    def suma(self):
        self.term += 1
        self.label.configure(text="%i %sC" % (self.term , self.gradeSymbol))
        
    def resta(self):
        self.term -= 1
        self.label.configure(text="%i %sC" % (self.term , self.gradeSymbol))  



class TestThreadingTemp(object):
    def __init__(self, interval=1):
        self.interval = interval

        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True
        thread.start()

    def run(self):
        global temperatura
        global humitat
        
        while True:
            # More statements comes here

            #Captura dades
            
            humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
            if humidity is not None and temperature is not None:
                print("Temp={0:0.2f}*C Humidity={1:0.1f}%".format(temperature, humidity))
                humitat= humidity
                temperatura= temperature-2
            else:
                print("Failed to get reading. Try again!")
            time.sleep(self.interval)




if __name__ == "__main__":
    root = tk.Tk()
    timer = Timer(root)
    root.attributes("-fullscreen", True)
    root.configure(background='black')
    root.bind("<Escape>", quit)
    root.bind("x", quit)
    root.config(cursor='none')
    
    #Corrriente pin 13
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(13,GPIO.OUT)
    GPIO.output(13,GPIO.HIGH)
    
    sensor = Adafruit_DHT.DHT11
    pin = 26
    
    
    
    tr = TestThreadingTemp()
    
    
    root.mainloop()