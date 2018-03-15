import os
import csv
from math import e
import numpy as np




with open ("data/newdata1125/merge.txt","r") as csvfile:
    Data = [list(map(float,rec)) for rec in csv.reader(csvfile,delimiter=",")]

for i in range(0,len(Data)):
    value=[]
    temp=Data[i][1:]   
    fft = np.fft.fft(temp)
    for j in range(0,len(fft)):
        distanceOfComplex = (fft[j].real**2+fft[j].imag**2)**0.5
        value.append(distanceOfComplex)
    print len(value)



      
  