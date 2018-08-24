import os
import csv
import numpy as np
import matplotlib.pyplot as plt

# global
folder = 'D:/temp/'

# parser for vibration.
def parser(data,label):
    # variable.
    pvdf1=[]
    pvdf2=[]
    pvdf3=[]
    for x in range (1,len(data),10000):
        temp_pvdf1 = [label]
        temp_pvdf2 = [label]
        temp_pvdf3 = [label]
        for y in range (0,10000):
            temp_pvdf1.append(float(data[x+y][1]))
            temp_pvdf2.append(float(data[x+y][2]))
            temp_pvdf3.append(float(data[x+y][3]))
        pvdf1.append(temp_pvdf1)
        pvdf2.append(temp_pvdf2)
        pvdf3.append(temp_pvdf3)
    return pvdf1, pvdf2, pvdf3

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
    for filename in FileNames:
        with open (folder+filename,"r") as file:
            Data = list(csv.reader(file,delimiter="\t"))
        pvdf1,pvdf2,pvdf3 = parser(Data,0)
    
        #save.
        ## pvdf1.
        pvdf1_file = open(folder+"pvdf1.txt", 'w+',encoding='utf8',newline='')
        Writer = csv.writer(pvdf1_file)
        Writer.writerows(pvdf1)
        pvdf1_file.close()

        ## pvdf2.
        pvdf2_file = open(folder+"pvdf2.txt", 'w+',encoding='utf8',newline='')
        Writer = csv.writer(pvdf2_file)
        Writer.writerows(pvdf2)
        pvdf2_file.close()

        ## pvdf3.
        pvdf3_file = open(folder+"pvdf3.txt", 'w+',encoding='utf8',newline='')
        Writer = csv.writer(pvdf3_file)
        Writer.writerows(pvdf3)
        pvdf3_file.close()







