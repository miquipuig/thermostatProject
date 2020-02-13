from Tkinter import * 
root = Tk()
from PIL import Image, ImageTk
import numpy as np
canvas = Canvas(root, width=500, height=500)
canvas.pack()
# caca = PhotoImage(file='/Users/miquel/raspberry/python/Pantalleta/images/power.png')
# canvas.create_image(250, 250, image=caca)

img= Image.open('images/power3.png')
img= img.resize((100, 100), Image.ANTIALIAS)
img2 = ImageTk.PhotoImage(img)
img.show()

im = img.convert('RGBA')
data1= np.array(im)
data2= np.array(im)
data3= np.array(im)  # "data" is a height x width x 4 numpy array
red, green, blue, alpha = data1.T # Temporarily unpack the bands for readability
red, green, blue, alpha = data2.T # Temporarily unpack the bands for readability
# Replace white with red... (leaves alpha values alone...)
defined_areas = (red == 0) & (blue == 222) & (green == 0)
data1[..., :-1][defined_areas.T] = (0, 0, 0) # Transpose back needed
data2[..., :-1][defined_areas.T] = (0, 255, 0)
data3[..., :-1][defined_areas.T] = (0, 0, 255)

# data1 = Image.fromarray(data1)
# im1=ImageTk.PhotoImage(data1)
# data2 = Image.fromarray(data2)
# im2=ImageTk.PhotoImage(data2)
# data3 = Image.fromarray(data3)
# im3=ImageTk.PhotoImage(data3)

canvas.create_image(100, 100, image=img2)
# canvas.create_image(200, 100, image=im1)
# canvas.create_image(300, 100, image=im2)
# canvas.create_image(400, 100, image=im3)


root.mainloop()