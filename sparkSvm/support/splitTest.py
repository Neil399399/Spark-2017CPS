import os
import csv

with open ("D:/News_Final.csv","r",encoding = 'utf8') as csvfile:
    Data= csv.reader(csvfile,delimiter=",")
    a = list(Data)

for y in range(0,len(a)):
    b=[x for x in a[y][2].split(" ")]
    print(b)

# with open ("Abnormal_2000RPM_1000.txt","r") as csvfile:
#     WData = [list(map(float,rec)) for rec in csv.reader(csvfile,delimiter="\t")]
#     for i in range(0,len(WData)):
#         WData[i].insert(0,0)
#     print(len(WData))

# #merge
# F= open('test(5).txt', 'wb')
# w = csv.writer(F)
# for x in range(800,1000):
#     a = Data[x]
#     b = WData[x]

#     w.writerows([a])
#     w.writerows([b])
# F.close()

# with open ("D:/CPS/rag-data/Train-1sec.txt","r") as csvfile:
#     z = [list(map(float,rec)) for rec in csv.reader(csvfile,delimiter="\t")]
    
#     print(len(z))
#     print(len(z[0]))

