from tkinter import *
from matplotlib.figure import Figure 
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, 
NavigationToolbar2Tk)  
import random
import math
import tkinter.font as font
import pyvisa
import time
from matplotlib import ticker
import numpy as np

rec = False
pltSec = False
filename = "5_11_dummy6.txt"

def recent():
    global rec
    global pltSec
    rec = True
    pltSec = False

def sec():
    global rec
    global pltSec
    pltSec = True
    rec = False
    
def base(): 
    global rec
    global pltSec
    rec = False
    pltSec = False

def plot():
    global output, fig
    clear_plot()
    
    fig = Figure(figsize = (w/100, h/100), dpi = 100)
    # adding the subplot 
    plot1 = fig.add_subplot(2,3,1) 
    plot2 = fig.add_subplot(2,3,2) 
    plot3 = fig.add_subplot(2,3,3) 
    plot4 = fig.add_subplot(2,3,4)
    plot5 = fig.add_subplot(2,3,5) 
    plot6 = fig.add_subplot(2,3,6)        

    # plotting the graph 
    plot1.plot(x, y1, '-')     
    plot2.plot(x, y2, '-')  
    plot3.plot(x, y3, '-')  
    plot4.plot(x, y4, '-') 
    plot5.plot(x, y5, '-')  
    plot6.plot(x, y6, '-')
    
    if(scaleBool[0] == True):
        plot1.set_ylim(mins[0], maxs[0])
    if(scaleBool[1] == True):
        plot2.set_ylim(mins[1], maxs[1])
    if(scaleBool[2] == True):
        plot3.set_ylim(mins[2], maxs[2])
    if(scaleBool[3] == True):
        plot4.set_ylim(mins[3], maxs[3])
    if(scaleBool[4] == True):
        plot5.set_ylim(mins[4], maxs[4])
    if(scaleBool[5] == True):
        plot6.set_ylim(mins[5], maxs[5])
    
    plot1.set_title('I')
    plot2.set_title('Temp')
    plot3.set_title('R SRS')
    plot4.set_title('Theta SRS')
    plot5.set_title('R DSP')
    plot6.set_title('Theta DSP')
    
    output = FigureCanvasTkAgg(fig, master = canvas)
    output.draw()

    # placing the canvas on the Tkinter window 
    output.get_tk_widget().pack()
    
def plotR():
    global output, fig
    clear_plot()
    
    vals = e1.get()
    try:
        val = int(vals)
    except ValueError:
        val = 0
    
    fig = Figure(figsize = (w/100, h/100), dpi = 100)
    # adding the subplot 
    plot1 = fig.add_subplot(2,3,1) 
    plot2 = fig.add_subplot(2,3,2) 
    plot3 = fig.add_subplot(2,3,3) 
    plot4 = fig.add_subplot(2,3,4)
    plot5 = fig.add_subplot(2,3,5) 
    plot6 = fig.add_subplot(2,3,6)        
    
    
    # plotting the graph
    PlotPart = True
    if(math.isnan(val)):
        PlotPart = False
    else:
        if(val < 2):
            PlotPart = False
        if(val > len(x)):
            PlotPart = False
    
    if(not PlotPart):
        plot1.plot(x, y1, '-')     
        plot2.plot(x, y2, '-')  
        plot3.plot(x, y3, '-')  
        plot4.plot(x, y4, '-') 
        plot5.plot(x, y5, '-')  
        plot6.plot(x, y6, '-')
        lab.config(text = 'Invalid Bound, Plotting All')
        
    else:
        plot1.plot(x[-val:], y1[-val:], '-')     
        plot2.plot(x[-val:], y2[-val:], '-')  
        plot3.plot(x[-val:], y3[-val:], '-')  
        plot4.plot(x[-val:], y4[-val:], '-') 
        plot5.plot(x[-val:], y5[-val:], '-')  
        plot6.plot(x[-val:], y6[-val:], '-')
        lab.config(text = 'Plotting Recent ' + str(val))
        
    if(scaleBool[0] == True):
        plot1.set_ylim(mins[0], maxs[0])
    if(scaleBool[1] == True):
        plot2.set_ylim(mins[1], maxs[1])
    if(scaleBool[2] == True):
        plot3.set_ylim(mins[2], maxs[2])
    if(scaleBool[3] == True):
        plot4.set_ylim(mins[3], maxs[3])
    if(scaleBool[4] == True):
        plot5.set_ylim(mins[4], maxs[4])
    if(scaleBool[5] == True):
        plot6.set_ylim(mins[5], maxs[5])
    
    plot1.set_title('I')
    plot2.set_title('Temp')
    plot3.set_title('R SRS')
    plot4.set_title('Theta SRS')
    plot5.set_title('R DSP')
    plot6.set_title('Theta DSP')
    
    output = FigureCanvasTkAgg(fig, master = canvas)
    output.draw()

    # placing the canvas on the Tkinter window 
    output.get_tk_widget().pack()

def plotSec():
    global output, fig
    global scaleBool
    global maxs
    global mins
    clear_plot()
    
    valL = e2.get()
    valR = e3.get()
    try:
        left = int(valL)
    except ValueError:
        left = 0
        
    try:
        right = int(valR)
    except ValueError:
        right = len(x)
    
    fig = Figure(figsize = (w/100, h/100), dpi = 100)
    # adding the subplot 
    plot1 = fig.add_subplot(2,3,1) 
    plot2 = fig.add_subplot(2,3,2) 
    plot3 = fig.add_subplot(2,3,3) 
    plot4 = fig.add_subplot(2,3,4)
    plot5 = fig.add_subplot(2,3,5) 
    plot6 = fig.add_subplot(2,3,6)        
    
    
    # plotting the graph
    PlotPart = True
    if(math.isnan(left) or math.isnan(right)):
        PlotPart = False
    else:
        if(left < 2 or right < 2):
            PlotPart = False
        if(left > len(x)):
            PlotPart = False
        if(right > len(x)):
            right = len(x)
        if(right - left < 2):
            PlotPart = False
    
    
    if(not PlotPart):
        plot1.plot(x, y1, '-')     
        plot2.plot(x, y2, '-')  
        plot3.plot(x, y3, '-')  
        plot4.plot(x, y4, '-') 
        plot5.plot(x, y5, '-')  
        plot6.plot(x, y6, '-')
        lab.config(text = 'Invalid Bounds, Plotting All')
        
    else:
        plot1.plot(x[left:right], y1[left:right], '-')     
        plot2.plot(x[left:right], y2[left:right], '-')  
        plot3.plot(x[left:right], y3[left:right], '-')  
        plot4.plot(x[left:right], y4[left:right], '-') 
        plot5.plot(x[left:right], y5[left:right], '-')  
        plot6.plot(x[left:right], y6[left:right], '-')
        lab.config(text = 'Plotting Section ' + str(left) + ' to ' + str(right))
        
    if(scaleBool[0] == True):
        plot1.set_ylim(mins[0], maxs[0])
    if(scaleBool[1] == True):
        plot2.set_ylim(mins[1], maxs[1])
    if(scaleBool[2] == True):
        plot3.set_ylim(mins[2], maxs[2])
    if(scaleBool[3] == True):
        plot4.set_ylim(mins[3], maxs[3])
    if(scaleBool[4] == True):
        plot5.set_ylim(mins[4], maxs[4])
    if(scaleBool[5] == True):
        plot6.set_ylim(mins[5], maxs[5])
    
    plot1.set_title('I')
    plot2.set_title('Temp')
    plot3.set_title('R SRS')
    plot4.set_title('Theta SRS')
    plot5.set_title('R DSP')
    plot6.set_title('Theta DSP')
    
    output = FigureCanvasTkAgg(fig, master = canvas)
    output.draw()

    # placing the canvas on the Tkinter window 
    output.get_tk_widget().pack()

def clear_plot():
    global output
    if output:
        for child in canvas.winfo_children():
            child.destroy()
        # or just use canvas.winfo_children()[0].destroy()  
  
    output = None
    
def reset():
    global scaleBool
    global maxs
    global mins
    scaleBool = [False]*6
    mins = [0]*6
    maxs = [0]*6
    
def takeScale():
    global scaleBool
    global maxs
    global mins
    index = e4.get()
    miv = e5.get()
    mav = e6.get()
    try:
        ind = int(index)
        mini = float(miv)
        maxi = float(mav)
        mins[ind] = mini
        maxs[ind] = maxi
        scaleBool[ind] = True
    except ValueError:
        print('Invalid Entry')
    
    
def get_data(index):
    loops = 5
    x.append(index)
    ret = [random.random(), random.random(), random.random(), random.random(), random.random(), random.random()]
    y1.append(ret[0])
    y2.append(ret[1])
    y3.append(ret[2])
    y4.append(ret[3])
    y5.append(ret[4])
    y6.append(ret[5])
    
    file = open(filename,"a")
    file.writelines(str(index) + ' ')
    for dat in ret:
        file.writelines(str(dat) + ' ')
    file.write("\n")
    file.close()
    
    if(index % loops == 0):
        if(rec == False and pltSec == False):
            plot()
            lab.config(text = 'Plotting All')
        if(rec == True and pltSec == False):
            plotR()
        if(pltSec == True):
            plotSec()
    window.after(1000, get_data, index + 1)
    

# the main Tkinter window 
window = Tk() 

output = None
fig = None

x = []
y1 = []
y2 = []
y3 = []
y4 = [] 
y5 = []
y6 = []
# setting the title 
window.title('Plotting in Tkinter') 

# dimensions of the main window 
window.geometry("1800x800") 

w = 1750
h = 750

scaleBool = [False]*6
mins = [0]*6
maxs = [0]*6

canvas = Canvas(window, width=w, height=h, bg='white') 
canvas.grid(row=0, column=0)

myFont = font.Font(family='Helvetica', size=20, weight='bold')
outFont = font.Font(family='Helvetica', size=20, weight='bold')

BB = Button(window, text="Plot All", command=base, bg='green', fg='white')
BB['font'] = myFont
BB.place(x=0, y=800)

myButton = Button(window, text="Plot Recent", command=recent, bg='yellow')
myButton['font'] = myFont
myButton.place(x=0, y=800)

e1 = Entry(window, width=10)
e1['font'] = outFont
e1.place(x=180, y=800)

But2 = Button(window, text="Plot From Index A to B", command=sec, bg='yellow')
But2['font'] = myFont
But2.place(x=340, y=800)

e2 = Entry(window, width=10)
e2['font'] = outFont
e2.place(x=660, y=800)

e3 = Entry(window, width=10)
e3['font'] = outFont
e3.place(x=810, y=800)

lab = Label(window, text='Plotting All', bg = 'light blue')
lab['font'] = myFont
lab.place(x=970, y=800)

clearScale = Button(window, text="Autoscale Plots", command=reset, bg='green', fg='white')
clearScale['font'] = myFont
clearScale.place(x=0, y=860)

TakeScale = Button(window, text="Take User Scale", command=takeScale, bg='blue', fg='white')
TakeScale['font'] = myFont
TakeScale.place(x=250, y=860)

e4 = Entry(window, width=10)
e4['font'] = outFont
e4.place(x=500, y=860)

e5 = Entry(window, width=10)
e5['font'] = outFont
e5.place(x=650, y=860)

e6 = Entry(window, width=10)
e6['font'] = outFont
e6.place(x=800, y=860)


window.after(100, get_data, 0)

# run the gui 
window.mainloop()