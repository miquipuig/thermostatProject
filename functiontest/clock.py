#simple clock program that shows in hours, minutes and seconds.
#Made in under 40 lines

import Tkinter
import time
# import time allows the program to get the time displayed on your computer.
TK_SILENCE_DEPRECATION=1
window = Tkinter.Tk()
window.wm_title('Digital Clock')
window.geometry('720x480')
time1 =''
# time1 directly takes the time in hours, minutes and seconds if available.
# clock = Tkinter.Label(window, font=('Trattatello', 140,), bg='black', fg='green')
# clock = Tkinter.Label(window, font=('Digital-7 Mono', 90,), bg='black', fg='green')
clock = Tkinter.Label(window, font=('Chocolate DRINK DEMO', 140,), bg='black', fg='green')
#To change the font, size, colour or bold text change the word inside the '   '.

# below is the function that allows the program to retrieve time globally meaning it will read outside the function.

def tick():
    global time1

    time2 = time.strftime('%-I:%M:%S')
    #time 2 will display on the clock that's why it's in Hours, minutes and seconds.
    #To change from AM/PM format, Just change the %-I to %H. The %M and %S are the same through both formats.
    if time2 != time1:
        time1= time2
        clock.config(text=time2)

    clock.after(200, tick)
tick()
clock.pack(fill='both',expand=1)
#window.mainloop continously loops the window
window.mainloop()