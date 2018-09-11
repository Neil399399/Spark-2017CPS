import os
import csv
from math import e
import numpy as np
import matplotlib.pyplot as plt


with open ("D:/temp2/pvdf2_spread_test_SVM.txt","r") as csvfile:
    Data = [list(map(float,rec)) for rec in csv.reader(csvfile,delimiter=",")]

    value=[]
    temp0=Data[1][1:]
    print(Data[1][0])
    temp1=Data[15][1:]
    print(Data[15][0])
    fft0 = np.fft.fft(temp0)/len(temp0)  
    fft1 = np.fft.fft(temp1)/len(temp1) 

    amplitude_0 = np.abs(fft0)
    amplitude_1 = np.abs(fft1)
    plt.plot(amplitude_0[0:200],label='line0',color='black')
    plt.plot(amplitude_1[0:200],label='line1',color='orange')
    plt.show()


      
  