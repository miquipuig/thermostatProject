from datetime import datetime,timedelta
import random
import numpy as np
historicData = [[],[],[],[]]

for i in range(10000):
    historicData[0].append(datetime.now()+timedelta(minutes=0.01*i)+timedelta(seconds=random.gauss(0,6))-timedelta(minutes=100000))
    historicData[1].append(20+random.gauss(-4,4))
    historicData[2].append(20+random.gauss(0,2))
    historicData[3].append(50+random.gauss(-50,50))

def round1min(tm):
        tm = tm+ timedelta(minutes=0.5)
        tm = tm-timedelta(minutes=tm.minute % 1, seconds=tm.second, microseconds=tm.microsecond)
        return tm
def round15min(tm):
        tm = tm+ timedelta(minutes=7.5)
        tm = tm-timedelta(minutes=tm.minute % 15, seconds=tm.second, microseconds=tm.microsecond)
        return tm

def roundTime(time,min):
    time = time+ timedelta(minutes=min/2)
    time = time-timedelta(minutes=tm.minute % min, seconds=time.second, microseconds=time.microsecond)
    return time

startT=datetime.now()
#i=start index of process
i=0
#last date parse
lastDate=datetime.now()-timedelta(minutes=60)
roundLastDate=round15min(lastDate)
compresshistoricData = [[],[],[],[]]
while(i<len(historicData[0]) and round15min(historicData[0][i])< roundLastDate):
    tm=round15min(historicData[0][i])
    tempData = []
    j=i
    while(i< len(historicData[0]) and round15min(historicData[0][i]) == tm and tm < roundLastDate):
        i+=1
    compresshistoricData[0].append(tm)
    compresshistoricData[1].append(np.around(np.mean(historicData[1][j:i]),decimals=1))
    compresshistoricData[2].append(np.around(np.mean(historicData[2][j:i]),decimals=1))
    compresshistoricData[3].append(np.around(np.mean(historicData[3][j:i]),decimals=1))
    # Delete
    historicData[0]=historicData[0][i:len(historicData[0])]
    historicData[1]=historicData[1][i:len(historicData[1])]
    historicData[2]=historicData[2][i:len(historicData[2])]
    historicData[3]=historicData[3][i:len(historicData[3])]
    #reset index
    i=0

# Concatenate
historicData[0]=compresshistoricData[0]+historicData[0]
historicData[1]=compresshistoricData[1]+historicData[1]
historicData[2]=compresshistoricData[2]+historicData[2]
historicData[3]=compresshistoricData[3]+historicData[3]
# print(historicData)

#save data
historicFile=open('historicData.csv','w')
for i in range(len(compresshistoricData[0])):
    historicFile.write(compresshistoricData[0][i].strftime("%Y-%m-%d %H:%M:%S"))
    historicFile.write(',')
    historicFile.write(str(compresshistoricData[1][i]))
    historicFile.write(',')
    historicFile.write(str(compresshistoricData[2][i]))
    historicFile.write(',')
    historicFile.write(str(compresshistoricData[3][i]))
    historicFile.write('\n')
     
historicFile.close()

readcompresshistoricData = [[],[],[],[]]
params=[4]
historicFile=open('historicData.csv','r')
lines=historicFile.read().split('\n')
for z in range(len(lines)-1):
    params=lines[z].split(',')
    readcompresshistoricData[0].append(datetime.strptime(params[0], "%Y-%m-%d %H:%M:%S"))
    readcompresshistoricData[1].append(params[1])
    readcompresshistoricData[2].append(params[2])
    readcompresshistoricData[3].append(params[3])
historicFile.close()

print('End process')
print(datetime.now()-startT)
print('-------------')
