import os
import csv
import numpy as np
import matplotlib.pyplot as plt

# global
folder = 'D:/temp/'
output_folder = 'D:/temp2/'

# parser for vibration.
def parser(data):
    # variable.
    pvdf1=[]
    pvdf2=[]
    pvdf3=[]
    for x in range (1,len(data),10000):
        temp_pvdf1=[]
        temp_pvdf2=[]
        temp_pvdf3=[]
        for y in range (0,10000):
            temp_pvdf1.append(float(data[x+y][1]))
            temp_pvdf2.append(float(data[x+y][2]))
            temp_pvdf3.append(float(data[x+y][3]))
        pvdf1.append(temp_pvdf1)
        pvdf2.append(temp_pvdf2)
        pvdf3.append(temp_pvdf3)
    return pvdf1, pvdf2, pvdf3

    
if __name__ == "__main__":

    # search all file in folder.
    FileNames=[]
    for root,dirs,files in os.walk(folder):
        for filename in files:
            FileNames.append(filename)
            
    for filename in FileNames:
        print(filename)
        with open (folder+filename,"r") as file:
            Data = list(csv.reader(file,delimiter="\t"))
        pvdf1,pvdf2,pvdf3 = parser(Data)

        print(len(pvdf2))









