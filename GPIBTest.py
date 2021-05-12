# -*- coding: utf-8 -*-
"""
Created on Wed May  5 22:45:52 2021

@author: sammy
"""


import pyvisa
import time
import numpy as np

def open(rm):
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
    dspR = float(vals[0])
    dspT = float(vals[1])
    
    tempA = therm.query('INPUT A:TEMPER?')
    
    isou.clear()
    Inow = isou.query('R0\r')
    istuff = Inow.split("R")
    Ival = float(istuff[1])
    
    retVal = [Ival, tempA, srsR, srsT, dspR, dspT]
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
        
def startRamp(isou):
    isou.write('A0\r')
    isou.read()
    isou.write('A1\r')
    isou.read()
    
def hold(isou):
    isou.write('A0\r')
    isou.read()

Iset = 1.0
booli = True
rm = pyvisa.ResourceManager()
print(rm.list_resources())
srs, dsp, therm, isou = open(rm)
isou.clear()
setMax(isou, Iset)
setSign(isou, booli)
startRamp(isou)
for i  in range(0, 100):
    ret = getData(srs, dsp, therm, isou)
    print(ret)
    if(np.abs(ret[0]) == Iset):
        booli = not booli
        setSign(isou, booli)
        startRamp(isou)
    time.sleep(1)
hold(isou)