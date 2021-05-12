# -*- coding: utf-8 -*-
"""
Created on Tue May 11 15:03:20 2021

@author: sammy
"""
import numpy as np
import matplotlib.pyplot as plt

fname = 'C:/Users/sammy/Downloads/5_11_dummy6.txt'
Fdat = np.loadtxt(fname)
temps = Fdat[:, 2]
runs = Fdat[:, 0]

plt.plot(runs, temps)
plt.show()