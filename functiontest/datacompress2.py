#Faster data structre and manipulation
from datetime import datetime,timedelta
import random
import numpy as np
historicData = []

#Total data and data range
for i in range(10000):
    historicData.append([datetime.now()+timedelta(minutes=0.1*i)+timedelta(seconds=random.gauss(0,6))-timedelta(minutes=100000),20+random.gauss(-4,4),20+random.gauss(0,2),50+random.gauss(-50,50)])

def round1min(tm):
        tm = tm+timedelta(minutes=0.5)
        tm = tm-timedelta(minutes=tm.minute % 1, seconds=tm.second, microseconds=tm.microsecond)
        return tm
def round15min(tm):
        tm = tm+ timedelta(minutes=7.5)
        tm = tm-timedelta(minutes=tm.minute % 15, seconds=tm.second, microseconds=tm.microsecond)
        return tm

def roundTime(time,min):
    time = time+ timedelta(minutes=min/2)
    time = time-timedelta(minutes=time.minute % min, seconds=time.second, microseconds=time.microsecond)
    return time

def meanData(tm, section):
    data1, data2, data3 = ([] for i in range(3))
    for x in range(len(section)):
        data1.append(section[x][1])
        data2.append(section[x][2])
        data3.append(section[x][3])
    return [tm,np.around(np.mean(data1),decimals=1),np.around(np.mean(data2),decimals=1),np.around(np.mean(data3),decimals=1)]

startT=datetime.now()
#i=start index of process
i=0
#last date parse
lastDate=datetime.now()-timedelta(minutes=0)
roundLastDate=roundTime(lastDate,15)
compresshistoricData = []
while(i<len(historicData) and roundTime(historicData[i][0],15)< roundLastDate):
    tm=roundTime(historicData[i][0],15)
    j=i
    while(i<len(historicData) and roundTime(historicData[i][0],15) == tm and tm < roundLastDate):
        i+=1
    compresshistoricData.append(meanData(tm,historicData[j:i]))
    # Delete
    historicData=historicData[i:len(historicData)]
    #reset index
    i=0

# Concatenate
historicData=compresshistoricData+historicData

# save data
historicFile=open('historicData.csv','w')
for i in range(len(compresshistoricData)):
    historicFile.write(compresshistoricData[i][0].strftime("%Y-%m-%d %H:%M:%S"))
    historicFile.write(',')
    historicFile.write(str(compresshistoricData[i][1]))
    historicFile.write(',')
    historicFile.write(str(compresshistoricData[i][2]))
    historicFile.write(',')
    historicFile.write(str(compresshistoricData[i][3]))
    historicFile.write('\n')

historicFile.close()

readcompresshistoricData = []
historicFile=open('historicData.csv','r')
lines=historicFile.read().split('\n')
for z in range(len(lines)-1):
    params=lines[z].split(',')
    readcompresshistoricData.append([datetime.strptime(params[0], "%Y-%m-%d %H:%M:%S"),params[1],params[2],params[3]])
historicFile.close()

print('End process')
print(datetime.now()-startT)
print('-------------')
