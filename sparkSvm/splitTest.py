import os
import csv

with open ("Normal_2000RPM_1000.txt","r") as csvfile:
    Data= [list(map(float,rec)) for rec in csv.reader(csvfile,delimiter="\t")]
    for i in range(0,len(Data)):
        Data[i].insert(0,1)
    print(len(Data))



with open ("Abnormal_2000RPM_1000.txt","r") as csvfile:
    WData = [list(map(float,rec)) for rec in csv.reader(csvfile,delimiter="\t")]
    for i in range(0,len(WData)):
        WData[i].insert(0,0)
    print(len(WData))

#merge
F= open('test(5).txt', 'wb')
w = csv.writer(F)
for x in range(800,1000):
    a = Data[x]
    b = WData[x]

    w.writerows([a])
    w.writerows([b])
F.close()

# with open ("test(1600-2000).txt","r") as csvfile:
#     z = [list(map(float,rec)) for rec in csv.reader(csvfile,delimiter=",")]
    
#     print(len(z))
#     print(len(z[0]))

