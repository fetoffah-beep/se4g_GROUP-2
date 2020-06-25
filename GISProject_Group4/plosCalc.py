# -*- coding: utf-8 -*-
"""
Created on Sat Jun  6 17:29:03 2020

@author: 39351
"""
import math
def plosCalc(Vm, Nt, Sr, Wv, W1, ppk, Wbuf, fb, WaA, fsw):
    a= Vm / (4 * Nt)
    b= (Sr * 0.621371)^2 / 100
    c= Wv * 3.28084
    d= W1 * 3.28084
    e= ppk
    f= Wbuf * 3.28084
    g= fb
    h= WaA * 3.28084
    i= fsw
    if h>10:
        i = 6-0.3*10
    elif h<10:
        i=6-0.3*h       
    plos = 6.0468 + (0.0091 * a) + (4 * b) - (1.2276 * math.log1p(c + (0.5 * d) + (50 * e) + (f * g) + (h * i)))     
    return plos