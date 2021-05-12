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
Iset = 1.0
booli = True

def openDev(rm):
    srs = rm.open_resource('GPIB0::10::INSTR')
    print(srs.query('*IDN?'))
    dsp = rm.open_resource('GPIB0::12::INSTR')
    print(dsp.query('*IDN?'))
    therm = rm.open_resource('GPIB0::13::INSTR')
    print(therm.query('*IDN?'))
    isou = rm.open_resource('GPIB0::25::INSTR')
    isou.read_termination = '\r'
    return srs, dsp, therm, isou

def getData(srs, dsp, therm, isou):
    srs.clear()
    srsR = float(srs.query('OUTP ? 3'))
    srsT = float(srs.query('OUTP ? 4'))
    
    dsp.clear()
    DSPstr = dsp.query('MP.')
    vals = DSPstr.split(",")
    try:
        dspR = float(vals[0])
        dspT = float(vals[1])
    except ValueError:
        dspR = 0.0
        dspT = 0.0
    
    tempA = float(therm.query('INPUT A:TEMPER?'))
    
    isou.clear()
    Inow = isou.query('R0\r')
    istuff = Inow.split("R")
    Ival = float(istuff[1])
    
    retVal = np.asarray([Ival, tempA, srsR, srsT, dspR, dspT], dtype=float)
    return retVal

def setMax(isou, maxi):
    stri = 'I' + str(maxi) + '\r'
    isou.write(stri)
    isou.read()
    
def setSign(isou, booli):
    if(booli):
        isou.write('P1\r')
        isou.read()
    else:
        isou.write('P2\r')
        isou.read()
    time.sleep(.25)
        
def startRamp(isou):
    isou.write('A0\r')
    isou.read()
    time.sleep(.25)
    isou.write('A1\r')
    isou.read()
    
def hold(isou):
    isou.write('A0\r')
    isou.read()
    
rm = pyvisa.ResourceManager()
print(rm.list_resources())
srs, dsp, therm, isou= openDev(rm)

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
    
def get_data(index):
    global booli
    global Iset
    loops = 5
    x.append(index)
    ret = getData(srs, dsp, therm, isou)
    y1.append(ret[0])
    y2.append(ret[1])
    y3.append(ret[2])
    y4.append(ret[3])
    y5.append(ret[4])
    y6.append(ret[5])
    
    if(np.abs(ret[0]) == Iset):
        booli = not booli
        setSign(isou, booli)
        startRamp(isou)
    
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

canvas = Canvas(window, width=w, height=h, bg='white') 
canvas.pack()

myFont = font.Font(family='Helvetica', size=20, weight='bold')
outFont = font.Font(family='Helvetica', size=20, weight='bold')

BB = Button(window, text="Plot All", command=base, bg='green', fg='white')
BB['font'] = myFont
BB.pack(side = LEFT)

myButton = Button(window, text="Plot Recent", command=recent, bg='yellow')
myButton['font'] = myFont
myButton.pack(side = LEFT)

e1 = Entry(window, width=10)
e1['font'] = outFont
e1.pack(side = LEFT)

But2 = Button(window, text="Plot From Index A to B", command=sec, bg='yellow')
But2['font'] = myFont
But2.pack(side = LEFT)

e2 = Entry(window, width=10)
e2['font'] = outFont
e2.pack(side = LEFT)

e3 = Entry(window, width=10)
e3['font'] = outFont
e3.pack(side = LEFT)

lab = Label(window, text='Plotting All', bg = 'light blue')
lab['font'] = myFont
lab.pack(side=LEFT)

window.after(100, get_data, 0)


setMax(isou, Iset)
time.sleep(.25)
setSign(isou, booli)
time.sleep(.25)
startRamp(isou)
time.sleep(.25)

# run the gui
window.mainloop()

hold(isou)