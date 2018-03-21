import os
import csv
from time import time

# parser for 1 sec 1000.
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
    #1~1001
    for x in range (1,1001):
        vibration1.append(float(a[x][1]))
        temp1_outdoor_temperature = temp1_outdoor_temperature + float(a[x][2])
        temp1_indoor_temperature = temp1_indoor_temperature + float(a[x][3])
    #average temperature
    outdoor1_temperature = temp1_outdoor_temperature/1000
    indoor1_temperature = temp1_indoor_temperature/1000
    #append tenperature after vibration
    vibration1.append(outdoor1_temperature)
    vibration1.append(indoor1_temperature)
    #insert label
    if (label==1):
        vibration1.insert(0,1)
    else:
        vibration1.insert(0,0) 

    #1001~2001
    for x in range (1001,2001):
        vibration2.append(float(a[x][1]))
        temp2_outdoor_temperature = temp2_outdoor_temperature + float(a[x][2])
        temp2_indoor_temperature = temp2_indoor_temperature + float(a[x][3])

    outdoor2_temperature = temp2_outdoor_temperature/1000
    indoor2_temperature = temp2_indoor_temperature/1000

    vibration2.append(outdoor2_temperature)
    vibration2.append(indoor2_temperature)
    if (label==1):
        vibration2.insert(0,1)
    else:
        vibration2.insert(0,0)


    #2001~3001
    for x in range (2001,3001):
        vibration3.append(float(a[x][1]))
        temp3_outdoor_temperature = temp3_outdoor_temperature + float(a[x][2])
        temp3_indoor_temperature = temp3_indoor_temperature + float(a[x][3])

    outdoor3_temperature = temp3_outdoor_temperature/1000
    indoor3_temperature = temp3_indoor_temperature/1000

    vibration3.append(outdoor3_temperature)
    vibration3.append(indoor3_temperature)
    if (label==1):
        vibration3.insert(0,1)
    else:
        vibration3.insert(0,0)
    
    #3001~4001
    for x in range (3001,4001):
        vibration4.append(float(a[x][1]))
        temp4_outdoor_temperature = temp4_outdoor_temperature + float(a[x][2])
        temp4_indoor_temperature = temp4_indoor_temperature + float(a[x][3])

    outdoor4_temperature = temp4_outdoor_temperature/1000
    indoor4_temperature = temp4_indoor_temperature/1000

    vibration4.append(outdoor4_temperature)
    vibration4.append(indoor4_temperature)
    if (label==1):
        vibration4.insert(0,1)
    else:
        vibration4.insert(0,0)

    #put together
    normal=[vibration1,vibration2,vibration3,vibration4]
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
    outdoor1_temperature = temp1_outdoor_temperature/4000
    indoor1_temperature = temp1_indoor_temperature/4000
    #append tenperature after vibration
    vibration1.append(outdoor1_temperature)
    vibration1.append(indoor1_temperature)
    #insert label
    if (label==1):
        vibration1.insert(0,1)
    else:
        vibration1.insert(0,0)
    #put together
    normal=[vibration1]
    return normal


print("parser start running!!")
# folder.
# NormalDir = 'C:/Users/User/Downloads/500rpm_one_bolt(new)/500rpm_one_bolt(new)/Data/'
# NormalDir = 'C:/Users/User/Downloads/500rpm_normal(new)/500rpm_normal(new)/Data/'
# unNormalDir ='C:/Users/User/Downloads/500rpm_rag(new)/Data/'
unNormalDir ='C:/Users/User/Downloads/500rpm_two_bolts(new)/500rpm_two_bolts(new)/Data/'

# TrainDir = 'D:/CPS/oneBlot-rag/oneBlot-ragTrain.txt'
# TestDir = 'D:/CPS/oneBlot-rag/oneBlot-ragTest.txt'
TrainDir = 'D:/CPS/abnormal/Train-1sec.txt'
TestDir = 'D:/CPS/abnormal/Test-1sec.txt'

startTime = time()

# select all the file in folder and save in the list.
# Normal dataset.
# normalFilenames=[]
# for root,dirs,files in os.walk(NormalDir):
    # for filename in files:
    #     normalFilenames.append(filename)

# normalFileAmounts = len(normalFilenames)
# print("File amounts in NormalDir:",normalFileAmounts)

# unNormal dataset.
unNormalFilenames=[]
for root,dirs,files in os.walk(unNormalDir):
    for filename in files:
        unNormalFilenames.append(filename)

unNormalFileAmounts = len(unNormalFilenames)
print("File amounts in unNormalDir:",unNormalFileAmounts)

#merge
Train= open(TrainDir, 'a')
Test= open(TestDir, 'a')

wtrain = csv.writer(Train)
wtest = csv.writer(Test)

#for training(Normal)
# for i in range (0,int(normalFileAmounts*3/4)):
#     print("start make train data ...")
#     print("file number:",i)
#    #open
#     with open (NormalDir+normalFilenames[i],"r") as file:
#         Data = csv.reader(file,delimiter="\t")
#         a = list(Data)
    
#     normal=parser(a,1)
#     wtrain.writerows(normal)

#for training(unNormal)
for i in range (0,int(unNormalFileAmounts*3/4)):
    print("start make train data(unNormal) ...")
    print("file number:",i)
   #open
    with open (unNormalDir+unNormalFilenames[i],"r") as file:
        Data = csv.reader(file,delimiter="\t")
        a = list(Data)
    
    unNormal=parser(a,0)
    wtrain.writerows(unNormal)

Train.close()

# #for testing(Normal)
# for i in range (int(normalFileAmounts*3/4),normalFileAmounts):
#     print("start make test data ...")
#     print("file number:",i)
#    #open
#     with open (NormalDir+normalFilenames[i],"r") as file:
#         Data = csv.reader(file,delimiter="\t")
#         a = list(Data)

    
#     normal=parser(a,1)
#     wtest.writerows(normal)


#for testing(unNormal)
for i in range (int(unNormalFileAmounts*3/4),unNormalFileAmounts):
    print("start make test data(unNormal) ...")
    print("file number:",i)
   #open
    with open (unNormalDir+unNormalFilenames[i],"r") as file:
        Data = csv.reader(file,delimiter="\t")
        a = list(Data)
    
    unNormal=parser(a,0)
    wtest.writerows(unNormal)

Test.close()

endTime = time()
runningTime = endTime - startTime
print("parser finished !!\n Running Time:"+str(runningTime))

