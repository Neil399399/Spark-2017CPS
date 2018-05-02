import os
import csv
from time import time


def parserOfMotorPlatform(a,label):
    #insert label
    if (label==1):
        for x in range (0,len(a)):
            a[x].insert(0,1)
    else:
        for x in range (0,len(a)):
            a[x].insert(0,0)
    return a

print("parser start running!!")
# folder.
NormalDir ='D:/CPS/motor_platform/Data/1000RPM/1out/'
unNormalDir ='D:/CPS/motor_platform/Data/2000RPM/2out/'


TrainDir = 'D:/CPS/motor_platform/Data/2000RPM/Train-N1.txt'
TestDir = 'D:/CPS/motor_platform/Data/2000RPM/Test-N1.txt'

startTime = time()

origin_file =["1out_1500RPM_snew.csv","2out_2000RPM_snew.csv"]
#merge
Train= open(TrainDir, 'a')
Test= open(TestDir, 'a')

wtrain = csv.writer(Train)
wtest = csv.writer(Test)

#for training(Normal)
#open
with open (NormalDir+origin_file[0],"r") as file:
    Data = csv.reader(file,delimiter=",")
    a = list(Data)

normal=parserOfMotorPlatform(a,1)
# 3/4 of origin data for training.
print("start make train data (Normal) ...")
wtrain.writerows(normal[0:749])
print("start make test data (Normal) ...")
wtest.writerows(normal[750:999])

# for training(unNormal)
#open
with open (unNormalDir+origin_file[1],"r") as file:
    Data = csv.reader(file,delimiter=",")
    a = list(Data)

unNormal=parserOfMotorPlatform(a,0)
print("start make train data (unNormal) ...")
wtrain.writerows(unNormal[0:749])
print("start make test data (unNormal) ...")
wtest.writerows(unNormal[750:999])

Train.close()
Test.close()

endTime = time()
runningTime = endTime - startTime
print("parser finished !!\n Running Time:"+str(runningTime))

