import os
import csv
from time import time

# parser for 1 sec 1652, but we just need half of row, so we take 1 sec 826.
def parser(a,label):
    temp1_outdoor_temperature =0.00
    temp2_outdoor_temperature =0.00
    temp3_outdoor_temperature =0.00
    temp4_outdoor_temperature =0.00
    temp1_indoor_temperature =0.00
    temp2_indoor_temperature =0.00
    temp3_indoor_temperature =0.00
    temp4_indoor_temperature =0.00
    vibration1=[]
    vibration2=[]
    vibration3=[]
    vibration4=[]
    #1~1623
    for x in range (1,1652):
        vibration1.append(float(a[x][1]))
        temp1_outdoor_temperature = temp1_outdoor_temperature + float(a[x][2])
        temp1_indoor_temperature = temp1_indoor_temperature + float(a[x][3])
    #average temperature
    outdoor1_temperature = temp1_outdoor_temperature/1651
    indoor1_temperature = temp1_indoor_temperature/1651
    #append tenperature after vibration
    vibration1.append(outdoor1_temperature)
    vibration1.append(indoor1_temperature)
    #insert label
    if (label==0):
        vibration1.insert(0,0)
    elif (label==1):
        vibration1.insert(0,1)
    elif (label==2):
        vibration1.insert(0,2)
    elif (label==3):    
        vibration1.insert(0,3) 

    #1653~3305
    for x in range (1652,3303):
        vibration2.append(float(a[x][1]))
        temp2_outdoor_temperature = temp2_outdoor_temperature + float(a[x][2])
        temp2_indoor_temperature = temp2_indoor_temperature + float(a[x][3])

    outdoor2_temperature = temp2_outdoor_temperature/1651
    indoor2_temperature = temp2_indoor_temperature/1651

    vibration2.append(outdoor2_temperature)
    vibration2.append(indoor2_temperature)
    if (label==0):
        vibration2.insert(0,0)
    elif (label==1):
        vibration2.insert(0,1)
    elif (label==2):
        vibration2.insert(0,2)
    elif (label==3):    
        vibration2.insert(0,3) 


    #3306~4958
    for x in range (3303,4954):
        vibration3.append(float(a[x][1]))
        temp3_outdoor_temperature = temp3_outdoor_temperature + float(a[x][2])
        temp3_indoor_temperature = temp3_indoor_temperature + float(a[x][3])

    outdoor3_temperature = temp3_outdoor_temperature/1651
    indoor3_temperature = temp3_indoor_temperature/1651

    vibration3.append(outdoor3_temperature)
    vibration3.append(indoor3_temperature)
    if (label==0):
        vibration3.insert(0,0)
    elif (label==1):
        vibration3.insert(0,1)
    elif (label==2):
        vibration3.insert(0,2)
    elif (label==3):    
        vibration3.insert(0,3) 
    
    # #4959~5783
    # for x in range (4957,6609):
    #     vibration4.append(float(a[x][1]))
    #     temp4_outdoor_temperature = temp4_outdoor_temperature + float(a[x][2])
    #     temp4_indoor_temperature = temp4_indoor_temperature + float(a[x][3])

    # outdoor4_temperature = temp4_outdoor_temperature/1652
    # indoor4_temperature = temp4_indoor_temperature/1652

    # vibration4.append(outdoor4_temperature)
    # vibration4.append(indoor4_temperature)
    # if (label==0):
    #     vibration4.insert(0,0)
    # elif (label==1):
    #     vibration4.insert(0,1)
    # elif (label==2):
    #     vibration4.insert(0,2)
    # elif (label==3):    
    #     vibration4.insert(0,3) 

    #put together
    normal=[vibration1,vibration2,vibration3]
    print(len(vibration2))
    return normal

# parser for 1 sec 4000.
def parserOneFile(a,label):
    temp1_outdoor_temperature =0.00
    temp1_indoor_temperature =0.00
    vibration1=[]
    #1~4001
    for x in range (1,4001):
        vibration1.append(float(a[x][1]))
        temp1_outdoor_temperature = temp1_outdoor_temperature + float(a[x][2])
        temp1_indoor_temperature = temp1_indoor_temperature + float(a[x][3])
    #average temperature
    outdoor1_temperature = temp1_outdoor_temperature/1652
    indoor1_temperature = temp1_indoor_temperature/1652
    #append tenperature after vibration
    vibration1.append(outdoor1_temperature)
    vibration1.append(indoor1_temperature)
    #insert label
    if (label==0):
        vibration1.insert(0,0)
    elif (label==1):
        vibration1.insert(0,1)
    elif (label==2):
        vibration1.insert(0,2)
    elif (label==3):    
        vibration1.insert(0,3) 
    #put together
    normal=[vibration1]
    return normal

def mold(a,label):
    vibration1=[]
    #1~826
    for i in range(1,len(a),1651):
        temp =[]
        for x in range (i,i+824):
            temp.append(float(a[x][1]))
        #insert label
        if (label==1):
            temp.insert(0,1)
        else:
            temp.insert(0,0)
    #put together
        vibration1.append(temp)
    return vibration1




print("parser start running!!")
# folder.
NormalDir = 'C:/Users/User/Downloads/Data-20180714T083321Z-001/Data/'
oneBoltDir = 'C:/Users/User/Downloads/20180715-onebolt/Data/'
twoBoltDir = 'C:/Users/User/Downloads/20180720-twobolt/Data/'
ragDir = 'C:/Users/User/Downloads/20180725-rag/Data/'

# NormalDir ='C:/Users/User/Downloads/500rpm_rag(new)/Data/'
# unNormalDir ='C:/Users/User/Downloads/500rpm_two_bolts(new)/500rpm_two_bolts(new)/Data/'

TrainDir = 'D:/CPS/Random_forest_train.txt'
TestDir = 'D:/CPS/Random_forest_test.txt'
# TrainDir = 'D:/CPS/random_forest_train1.txt'
# TestDir = 'D:/CPS/random_forest_test1.txt'

startTime = time()

# select all the file in folder and save in the list.
# Normal dataset.
normalFilenames=[]
for root,dirs,files in os.walk(NormalDir):
    for filename in files:
        normalFilenames.append(filename)

normalFileAmounts = len(normalFilenames)
print("File amounts in NormalDir:",normalFileAmounts)

# onebolt dataset.
oneBoltFilenames=[]
for root,dirs,files in os.walk(oneBoltDir):
    for filename in files:
        oneBoltFilenames.append(filename)

oneBoltFileAmounts = len(oneBoltFilenames)
print("File amounts in oneboltDir:",oneBoltFileAmounts)

# twobolt dataset.
twoBoltFilenames=[]
for root,dirs,files in os.walk(twoBoltDir):
    for filename in files:
        twoBoltFilenames.append(filename)

twoBoltFileAmounts = len(twoBoltFilenames)
print("File amounts in twoboltDir:",twoBoltFileAmounts)

# rag dataset.
ragFilenames=[]
for root,dirs,files in os.walk(ragDir):
    for filename in files:
        ragFilenames.append(filename)

ragFileAmounts = len(ragFilenames)
print("File amounts in ragDir:",ragFileAmounts)
####################################################################
#merge
Train= open(TrainDir, 'a')
Test= open(TestDir, 'a')

wtrain = csv.writer(Train)
wtest = csv.writer(Test)


########################## train ###########################
#for training(Normal)
for i in range (0,int(normalFileAmounts*3/4)):
    print("start make train data(Normal) ...")
    print("file number:",i)
   #open
    with open (NormalDir+normalFilenames[i],"r") as file:
        Data = csv.reader(file,delimiter="\t")
        a = list(Data)


    
    normal=parser(a,0)
    wtrain.writerows(normal)

#for training(onebolt)
for i in range (0,int(oneBoltFileAmounts*3/4)):
    print("start make train data(onebolt) ...")
    print("file number:",i)
   #open
    with open (oneBoltDir+oneBoltFilenames[i],"r") as file:
        Data = csv.reader(file,delimiter="\t")
        b = list(Data)
    
    oneBolt=parser(b,1)
    wtrain.writerows(oneBolt)

#for training(twobolt)
for i in range (0,int(twoBoltFileAmounts*3/4)):
    print("start make train data(twobolt) ...")
    print("file number:",i)
   #open
    with open (twoBoltDir+twoBoltFilenames[i],"r") as file:
        Data = csv.reader(file,delimiter="\t")
        c = list(Data)
    rwoBolt=parser(c,2)
    wtrain.writerows(rwoBolt)

#for training(rag)
for i in range (0,int(ragFileAmounts*3/4)):
    print("start make train data(rag) ...")
    print("file number:",i)
   #open
    with open (ragDir+ragFilenames[i],"r") as file:
        Data = csv.reader(file,delimiter="\t")
        d = list(Data)
    
    rag=parser(d,3)
    wtrain.writerows(rag)

Train.close()

######################### test ###########################
#for testing(Normal)
for i in range (int(normalFileAmounts*3/4),normalFileAmounts):
    print("start make test data(Normal) ...")
    print("file number:",i)
   #open
    with open (NormalDir+normalFilenames[i],"r") as file:
        Data = csv.reader(file,delimiter="\t")
        a = list(Data)

    normal=parser(a,0)
    wtest.writerows(normal)


#for testing(onebolt)
for i in range (int(oneBoltFileAmounts*3/4),oneBoltFileAmounts):
    print("start make test data(onebolt) ...")
    print("file number:",i)
   #open
    with open (oneBoltDir+oneBoltFilenames[i],"r") as file:
        Data = csv.reader(file,delimiter="\t")
        b = list(Data)
    
    oneBolt=parser(b,1)
    wtest.writerows(oneBolt)

#for testing(twobolt)
for i in range (int(twoBoltFileAmounts*3/4),twoBoltFileAmounts):
    print("start make test data(twobolt) ...")
    print("file number:",i)
   #open
    with open (twoBoltDir+twoBoltFilenames[i],"r") as file:
        Data = csv.reader(file,delimiter="\t")
        c = list(Data)
    
    rwoBolt=parser(c,2)
    wtest.writerows(rwoBolt)

#for testing(rag)
for i in range (int(ragFileAmounts*3/4),ragFileAmounts):
    print("start make test data(rag) ...")
    print("file number:",i)
   #open
    with open (ragDir+ragFilenames[i],"r") as file:
        Data = csv.reader(file,delimiter="\t")
        d = list(Data)
    
    rag=parser(d,3)
    wtest.writerows(rag)

Test.close()



endTime = time()
runningTime = endTime - startTime
print("parser finished !!\n Running Time:"+str(runningTime))

