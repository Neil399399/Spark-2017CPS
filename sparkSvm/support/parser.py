import os
import csv
import numpy as np
# global
folder = 'D:/temp/temp/'

# parser for vibration.
def parser(data):
    # variable.
    temp_outdoor_temperature = 0.00
    temp_indoor_temperature = 0.00
    vibration=[]
    #1~1652
    for x in range (1,1652):
        vibration.append(float(data[x][1]))
        temp_outdoor_temperature = temp_outdoor_temperature + float(data[x][2])
        temp_indoor_temperature = temp_indoor_temperature + float(data[x][3])
    #average temperature
    outdoor_temperature = temp_outdoor_temperature/1651
    indoor_temperature = temp_indoor_temperature/1651
    #append tenperature after vibration
    vibration.append(outdoor_temperature)
    vibration.append(indoor_temperature)
    return vibration

def feature(List):
    Complex = np.fft.fft(List[0:1650])
    feature = []
    # WSN header flag.
    feature.append('54')
    for i in range(0,30):
        temp = (Complex[i].real**2+Complex[i].imag**2)**0.5
        temp = "%.4f" %temp
        temp = temp.replace(".","")
        feature.append(temp)
    temp1 = "%.4f" %List[1651]
    temp2 = "%.4f" %List[1652]
    temp1 = temp1.replace(".","")
    temp2 = temp2.replace(".","")
    feature.append(temp1)
    feature.append(temp2)
    # WSN tail flag.
    feature.append('66')
    return [feature]
    
if __name__ == "__main__":

    FileNames=[]
    for root,dirs,files in os.walk(folder):
        for filename in files:
            FileNames.append(filename)
    
    for filename in FileNames:
        with open (folder+filename,"r") as file:
            Data = list(csv.reader(file,delimiter="\t"))
        features=feature(parser(Data))

        new_file = open(folder+"temp.txt", 'w+',encoding='utf8',newline='')
        Writer = csv.writer(new_file)
        Writer.writerows(features)
        new_file.close()
        ## wirte with '\n'
        # for x in features:
        #     print(x)
        #     new_file.writelines(x+'\n')
        # new_file.close()

