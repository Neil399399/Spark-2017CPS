import os
import csv
import numpy as np
import matplotlib.pyplot as plt

# global
folder = 'D:/temp/'

# parser for vibration.
def parser(data):
    # variable.
    pvdf1=[]
    pvdf2=[]
    #1~10001
    for x in range (1,10001):
        pvdf1.append(float(data[x][1]))
        pvdf2.append(float(data[x][2]))
    return pvdf1, pvdf2

def amplitude(List,Range):
    Complex = np.fft.fft(List)/len(List)
    amplitude = np.abs(Complex[0:Range])
    return amplitude

def plot_timeDomain(list_1,list_2,x_axis_range):
    # set x axis range initial figure.
    x = np.linspace(0,x_axis_range,x_axis_range)
    plt.figure()
    # first subplot.
    plt.subplot(211)
    plt.plot(x,list_1[0:x_axis_range],label='line 1',color='orange')
    # second subplot.
    plt.subplot(212)
    plt.plot(x,list_2[0:x_axis_range],label='line 2',color='blue')
    plt.show()

def plot_freqDomain(list_1,list_2,freq_range,x_axis_range):
    # set x axis range and initial figure.
    x = np.linspace(0,x_axis_range,x_axis_range)
    plt.figure()
    # count amplitude.
    list_1 = amplitude(list_1,freq_range)
    list_2 = amplitude(list_2,freq_range)
    # plot.
    plt.subplot(211)
    plt.plot(x,list_1[0:x_axis_range],label='line 1',color='orange')
    plt.subplot(212)
    plt.plot(x,list_2[0:x_axis_range],label='line 2',color='blue')
    plt.show()


    
if __name__ == "__main__":

    FileNames=[]
    for root,dirs,files in os.walk(folder):
        for filename in files:
            FileNames.append(filename)
    
    print(FileNames[0])
    with open (folder+FileNames[0],"r") as file:
        Data = list(csv.reader(file,delimiter="\t"))
    pvdf1,pvdf2 = parser(Data)

    print(FileNames[1])
    with open (folder+FileNames[1],"r") as file:
        Data = list(csv.reader(file,delimiter="\t"))
    bg_pvdf1,bg_pvdf2 = parser(Data)

    plot_timeDomain(pvdf1,bg_pvdf1,1000)
    plot_timeDomain(pvdf2,bg_pvdf2,1000)
    plot_freqDomain(pvdf1,bg_pvdf1,5000,60)
    plot_freqDomain(pvdf2,bg_pvdf2,5000,60)


